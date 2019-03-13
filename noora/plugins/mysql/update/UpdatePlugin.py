import os

from noora.version.Version import Version
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader

from noora.system import Ora
from noora.system import PropertyHelper
from noora.io.File import File

from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.exceptions.plugins.InvalidEnvironmentException import InvalidEnvironmentException
from noora.exceptions.plugins.InvalidVersionException import InvalidVersionException

from noora.connectors.MysqlConnector import MysqlConnector
from noora.connectors.ConnectionExecutor import ConnectionExecutor


class UpdatePlugin(object):
    def __init__(self):
        Plugin.__init__(self, "update", MysqlConnector())

    def parse_args(self, parser, args):
        parser.add_argument('-v', type=str, help='version', required=True)
        parser.add_argument('-h', type=str, help='host', required=True)
        parser.add_argument('-d', type=str, help='database', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        parser.add_argument('-a', type=str, help='alias', required=False)

        return parser.parse_args(args)

    def fail_on_invalid_environment(self, connector, executor, environment, properties):
        plugin_dir = properties.get('plugin.dir')
        properties['environment'] = environment
        script = File(os.path.join(plugin_dir, 'mysql', 'update', 'checkenvironment.sql'))
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
        script = File(os.path.join(plugin_dir, 'mysql', 'update', 'checkversion.sql'))
        executor['script'] = script
        connector.execute(executor, properties)
        if "(Code 1329)" in connector.get_result():
            raise InvalidVersionException("invalid version: {}".format(previous))

    def execute(self, arguments, properties):
        properties['create.dir'] = os.path.join(properties.get('current.dir'), 'create')
        properties['alter.dir'] = os.path.join(properties.get('current.dir'), 'alter')

        host = arguments.h
        Fail.fail_on_no_host(host)

        version = arguments.v
        Fail.fail_on_no_version(version)

        default_databases = properties.get('databases')
        databases = Ora.nvl(arguments.d, default_databases)
        Fail.fail_on_invalid_database(arguments.d, properties)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        objects = properties.get('create_objects')

        version_database = properties.get('version_database')

        alter_dir = properties.get('alter.dir')

        Fail.fail_on_unknown_version(version, properties)

        alias = arguments.a
        database_aliases = properties.get('database_aliases')
        Fail.fail_on_invalid_alias(alias, properties)

        # if an alias is given, only this database will be installed, other databases will be
        # ignored.
        if alias:
            print("using alias :" + alias)
            databases = [alias]

        # retrieve the user credentials for this database project.
        users = properties.get('mysql_users')

        # try to retrieve the users from the credentials file, when no users are configured in
        # myproject.json.
        if not users:
            # retrieve the name of this database project, introduced in version 1.0.12
            profile = PropertyHelper.get_profile(properties)
            if profile:
                users = profile.get('mysql_users')

        connector = self.get_connector()

        for database in databases:
            print("updating database '{db}' on host '{host}' using environment '{env}'".format(
                db=database, host=host, env=environment))

            executor = PropertyHelper.get_mysql_properties(users, host, database)

            database_folder = PropertyHelper.get_database_folder(database, database_aliases)

            if database == version_database:
                self.fail_on_invalid_environment(connector, executor, environment, properties)
                self.fail_on_invalid_version(connector, executor, version, properties)

            for obj in objects:
                # global ddl objects
                folder = File(os.path.join(alter_dir, version, database_folder, 'ddl', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(
                    os.path.join(alter_dir, version, database_folder, 'ddl', obj, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(alter_dir, version, database_folder, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(alter_dir, version, database_folder, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print("database '{}' updated".format(database))
