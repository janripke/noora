import os

from noora.version.version import Version
from noora.version.versions import Versions
from noora.version.version_loader import VersionLoader

from noora.system import ora
from noora.system import property_helper
from noora.io.file import File

from noora.plugins.mssql.mssql_plugin import MssqlPlugin
from noora.plugins.fails import Fail

from noora.connectors.connection_executor import ConnectionExecutor


class UpdatePlugin(MssqlPlugin):
    """This class provides functionality for updating a project to a specified version."""
    def _validate_and_prepare(self, properties, arguments):
        prepared_args = {}

        version = arguments.get('version')
        Fail.fail_on_no_version(version)
        Fail.fail_on_unknown_version(version, properties)
        prepared_args['version'] = version

        host = arguments.get('host')
        Fail.fail_on_no_host(host)
        Fail.fail_on_invalid_host(host, properties)
        prepared_args['host'] = host

        environment = arguments.get('environment')
        default_environment = properties.get('default_environment')
        environment = ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

        connection_string = arguments.get('connection_string')
        prepared_args['connection_string'] = property_helper.connection_credentials(connection_string)
        Fail.fail_on_host_mismatch(host, prepared_args['connection_string'])

        return prepared_args

    def fail_on_invalid_environment(self, properties, connector, executor, environment):
        plugin_dir = properties.get('plugin.dir')
        properties['environment'] = environment
        script = File(os.path.join(plugin_dir, 'mssql', 'update', 'checkenvironment.sql'))
        executor['script'] = script
        connector.execute(executor, properties)

    def fail_on_invalid_version(self, properties, connector, executor, version):
        plugin_dir = properties.get('plugin.dir')

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        v = Version(version)
        previous = versions.previous(v).get_value()

        properties['previous'] = previous
        script = File(os.path.join(plugin_dir, 'mssql', 'update', 'checkversion.sql'))
        executor['script'] = script
        connector.execute(executor, properties)

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

        schemes = properties.get('schemes')
        host = prepared_args['host']
        environment = prepared_args['environment']
        version = prepared_args['version']
        database = properties.get('database')
        objects = properties.get('create_objects')
        version_schema = properties.get('version_schema')
        alter_dir = properties.get('alter.dir')

        # retrieve the database connection credentials through
        # the commandline option --connection-string
        connection_string = prepared_args['connection_string']
        if connection_string:
            users = connection_string

        if not connection_string:
            # retrieve the user credentials for this database project.
            users = properties.get('mssql_users')

            # try to retrieve the users from the credentials file, when no users are configured in
            # myproject.json.
            if not users:
                # retrieve the name of this database project, introduced in version 1.0.12
                profile = property_helper.get_profile(properties)
                if profile:
                    users = profile.get('mssql_users')

        # fail when no users are found. This means that they are not set in myproject.json or
        # credentials.json
        Fail.fail_on_no_users(users)

        connector = self.get_connector()

        for schema in schemes:
            print("updating schema '{schema}' in database '{db}' "
                  "on host '{host}' using environment '{env}'".format(
                    schema=schema, db=database, host=host, env=environment))

            executor = property_helper.get_mssql_properties(users, host, database, schema)

            # database_folder = PropertyHelper.get_database_folder(database, database_aliases)

            if schema == version_schema:
                self.fail_on_invalid_environment(properties, connector, executor, environment)
                self.fail_on_invalid_version(properties, connector, executor, version)

            for obj in objects:
                # global ddl objects
                folder = File(os.path.join(alter_dir, version, schema, 'ddl', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(os.path.join(alter_dir, version, schema, 'ddl', obj, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(alter_dir, version, schema, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(alter_dir, version, schema, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print("database '{}' updated.".format(database))
