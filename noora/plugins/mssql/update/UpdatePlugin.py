import os
from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.connectors.MssqlConnector import MssqlConnector
from noora.io.File import File
from noora.plugins.mysql.update.UnknownVersionException import UnknownVersionException
from noora.plugins.mysql.update.InvalidEnvironmentException import InvalidEnvironmentException
from noora.plugins.mysql.update.InvalidVersionException import InvalidVersionException
from noora.system.Ora import Ora
from noora.system.PropertyHelper import PropertyHelper
from noora.version.Version import Version
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.connectors.ConnectionExecutor import ConnectionExecutor


class UpdatePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "update", MssqlConnector())

    def fail_on_unknown_version(self, version, properties):
        alter_dir = properties.get('alter.dir')
        version_dir = File(os.path.join(alter_dir, version))
        if not version_dir.exists():
            raise UnknownVersionException("unknown version folder", version)

    def fail_on_invalid_environment(self, connector, executor, environment, properties):
        plugin_dir = properties.get('plugin.dir')
        properties['environment'] = environment
        script = File(os.path.join(plugin_dir, 'mssql', 'update', 'checkenvironment.sql'))
        executor['script'] = script
        # connector.execute(executor, properties)
        # if "(Code 1329)" in connector.get_result():
        #     raise InvalidEnvironmentException("invalid environment", environment)

    def fail_on_invalid_version(self, connector, executor, version, properties):
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
        print executor
        connector.execute(executor, properties)
        # if "(Code 1329)" in connector.get_result():
        #     raise InvalidVersionException("invalid version", previous)

    def execute(self, arguments, properties):
        properties['create.dir'] = os.path.join(properties.get('current.dir'), 'create')
        properties['alter.dir'] = os.path.join(properties.get('current.dir'), 'alter')

        host = arguments.h
        Fail.fail_on_no_host(host)

        version = arguments.v
        Fail.fail_on_no_version(version)

        default_schemes = properties.get('schemes')
        schemes = Ora.nvl(arguments.s, default_schemes)
        Fail.fail_on_invalid_schema(arguments.s, properties)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        database = properties.get('database')
        objects = properties.get('create_objects')

        version_schema = properties.get('version_schema')

        alter_dir = properties.get('alter.dir')

        self.fail_on_unknown_version(version, properties)

        # retrieve the user credentials for this database project.
        users = properties.get('mssql_users')

        # try to retrieve the users from the credentials file, when no users are configured in myproject.json.
        if not users:
            # retrieve the name of this database project, introduced in version 1.0.12
            profile = PropertyHelper.get_profile(properties)
            if profile:
                users = profile.get('mssql_users')

        connector = self.get_connector()

        for schema in schemes:
            print "updating schema '" + schema + "' in database '" + database + "' on host '" + host + "' using environment '" + environment + "'"

            username = PropertyHelper.get_mssql_user(users, host, schema)
            password = PropertyHelper.get_mssql_password(users, host, schema)

            executor = dict()
            executor['host'] = host
            executor['database'] = database
            executor['username'] = username
            executor['password'] = password

            # database_folder = PropertyHelper.get_database_folder(database, database_aliases)

            if schema == version_schema:
                self.fail_on_invalid_environment(connector, executor, environment, properties)
                self.fail_on_invalid_version(connector, executor, version, properties)

            for object in objects:
                # global ddl objects
                folder = File(os.path.join(alter_dir, version, schema, 'ddl', object))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(os.path.join(alter_dir, version, schema, 'ddl', object, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(alter_dir, version, schema, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(alter_dir, version, schema, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print "database '" + database + "' updated."
