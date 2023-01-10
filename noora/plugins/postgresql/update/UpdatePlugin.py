import os

from noora.version.Version import Version
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader

from noora.system import Ora
from noora.system import PropertyHelper
from noora.io.File import File

from noora.plugins.postgresql.PGSQLPlugin import PGSQLPlugin
from noora.plugins.Fail import Fail
from noora.exceptions.plugins.InvalidEnvironmentException import InvalidEnvironmentException
from noora.exceptions.plugins.InvalidVersionException import InvalidVersionException

from noora.connectors.ConnectionExecutor import ConnectionExecutor


class UpdatePlugin(PGSQLPlugin):
    """This class provides functionality for updating a project to a specified version."""
    def _validate_and_prepare(self, properties, arguments):
        prepared_args = {}

        version = arguments.get('version')
        Fail.fail_on_no_version(version)
        Fail.fail_on_unknown_version(version, properties)
        prepared_args['version'] = version

        host = arguments.get('host')
        Fail.fail_on_no_host(host)
        prepared_args['host'] = host

        environment = arguments.get('environment')
        default_environment = properties.get('default_environment')
        environment = Ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

        prepared_args['connection_string'] = arguments.get('connection_string')

        alias = arguments.get('alias')
        Fail.fail_on_invalid_alias(alias, properties)
        # if an alias is given, only this database will be installed, other databases will be
        # ignored.
        if alias:
            print("using alias: {}".format(alias))
            prepared_args['databases'] = [alias]
        else:
            database = arguments.get('database')
            Fail.fail_on_invalid_database(database, properties)
            default_databases = properties.get('databases')
            databases = Ora.nvl(database, default_databases)
            prepared_args['databases'] = databases

        return prepared_args

    def fail_on_invalid_environment(self, connector, executor, environment, properties):
        plugin_dir = properties.get('plugin.dir')
        properties['environment'] = environment
        script = File(os.path.join(plugin_dir, 'postgresql', 'update', 'checkenvironment.sql'))
        executor['script'] = script
        connector.execute(executor, properties)
        if "(Code 1329)" in connector.get_result():
            raise InvalidEnvironmentException("invalid environment: {}".format(environment))

    def fail_on_invalid_version(self, connector, executor, version, properties):
        plugin_dir = properties.get('plugin.dir')

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        v = Version(version)
        previous = versions.previous(v).get_value()

        properties['previous'] = previous
        script = File(os.path.join(plugin_dir, 'postgresql', 'update', 'checkversion.sql'))
        executor['script'] = script
        connector.execute(executor, properties)
        if "(Code 1329)" in connector.get_result():
            raise InvalidVersionException("invalid version: {}".format(previous))

    def execute(self, properties, arguments):
        """
        Update database after checking if schema and environment are
        valid values. Also check that host is not on the block list and that
        the version to update to is valid

        :type properties: system.Properties.Properties
        :param properties: The project properties
        :type arguments: dict
        :param arguments: This dict contains the plugin arguments:

            * **version**: The version to update the database to;
            * **host**: The hostname that hosts the database to update;
            * **schema**: Schema to update (optional);
            * **environment**: Environment to update the database in (optional).
        """
        prepared_args = self._validate_and_prepare(properties, arguments)

        version = prepared_args['version']
        host = prepared_args['host']
        environment = prepared_args['environment']
        databases = properties.get('databases')

        objects = properties.get('create_objects')

        version_database = properties.get('version_database')

        alter_dir = properties.get('alter.dir')

        # retrieve the database connection credentials through
        # the commandline option --connection-string
        connection_string = prepared_args['connection_string']
        if connection_string:
            users = PropertyHelper.connection_credentials(connection_string)

        if not connection_string:
            # retrieve the user credentials for this database project.
            users = properties.get('postgresql_users')

            # try to retrieve the users from the credentials file, when no users are configured in
            # myproject.json.
            if not users:
                # retrieve the name of this database project, introduced in version 1.0.12
                profile = PropertyHelper.get_profile(properties)
                if profile:
                    users = profile.get('postgresql_users')

        connector = self.get_connector()

        for database in databases:
            print("updating database '{db}' on host '{host}' using environment '{env}'".format(
                db=database, host=host, env=environment))

            executor = PropertyHelper.get_mysql_properties(users, host, database)

            if database == version_database:
                self.fail_on_invalid_environment(connector, executor, environment, properties)
                self.fail_on_invalid_version(connector, executor, version, properties)

            for obj in objects:
                # global ddl objects
                folder = File(os.path.join(alter_dir, version, database, 'ddl', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(
                    os.path.join(alter_dir, version, database, 'ddl', obj, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(alter_dir, version, database, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(alter_dir, version, database, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print("database '{}' updated".format(database))
