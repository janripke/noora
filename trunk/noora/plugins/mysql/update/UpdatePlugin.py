import os
from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.connectors.MysqlConnector import MysqlConnector
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
        Plugin.__init__(self, "update", MysqlConnector())

    def fail_on_unknown_version(self, version, properties):
        alter_dir = properties.get_property('alter.dir')
        version_dir = File(os.path.join(alter_dir, version))
        if not version_dir.exists():
            raise UnknownVersionException("unknown version folder", version)

    def fail_on_invalid_environment(self, connector, executor, environment, properties):
        plugin_dir = properties.get_property('plugin.dir')
        properties.set_property('environment', environment)
        script = File(os.path.join(plugin_dir, 'mysql', 'update', 'checkenvironment.sql'))
        executor['script'] = script
        connector.execute(executor, properties)
        if "(Code 1329)" in connector.get_result():
            raise InvalidEnvironmentException("invalid environment", environment)

    def fail_on_invalid_version(self, connector, executor, version, properties):
        plugin_dir = properties.get_property('plugin.dir')

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        v = Version(version)
        previous = versions.previous(v).get_value()

        properties.set_property('previous', previous)
        script = File(os.path.join(plugin_dir, 'mysql', 'update', 'checkversion.sql'))
        executor['script'] = script
        connector.execute(executor, properties)
        if "(Code 1329)" in connector.get_result():
            raise InvalidVersionException("invalid version", previous)

    def execute(self, arguments, properties):
        properties.set_property('create.dir', os.path.join(properties.get_property('current.dir'), 'create'))
        properties.set_property('alter.dir', os.path.join(properties.get_property('current.dir'), 'alter'))

        host = arguments.h
        Fail.fail_on_no_host(host)

        version = arguments.v
        Fail.fail_on_no_version(version)

        default_databases = properties.get_property('databases')
        databases = Ora.nvl(arguments.d, default_databases)
        Fail.fail_on_invalid_database(arguments.d, properties)

        default_environment = properties.get_property('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        objects = properties.get_property('create_objects')

        version_database = properties.get_property('version_database')

        alter_dir = properties.get_property('alter.dir')

        self.fail_on_unknown_version(version, properties)

        alias = arguments.a
        database_aliases = properties.get_property('database_aliases')
        Fail.fail_on_invalid_alias(alias, properties)

        # if an alias is given, only this database will be installed, other databases will be ignored.
        if alias:
            print "using alias :" + alias
            databases = [alias]

        connector = self.get_connector()

        for database in databases:
            print "updating database '" + database + "' on host '" + host + "' using environment '" + environment + "'"

            users = properties.get_property('mysql_users')
            username = PropertyHelper.get_mysql_user(users, host, database)
            password = PropertyHelper.get_mysql_passwd(users, host, database)

            executor = {}
            executor['host'] = host
            executor['database'] = database
            executor['username'] = username
            executor['password'] = password

            database_folder = PropertyHelper.get_database_folder(database, database_aliases)

            if database == version_database:
                self.fail_on_invalid_environment(connector, executor, environment, properties)
                self.fail_on_invalid_version(connector, executor, version, properties)

            for object in objects:
                # global ddl objects
                folder = File(os.path.join(alter_dir, version, database_folder, 'ddl', object))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(os.path.join(alter_dir, version, database_folder, 'ddl', object, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(alter_dir, version, database_folder, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(alter_dir, version, database_folder, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print "database '" + database + "' updated."
