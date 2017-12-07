import os
from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.system.PropertyHelper import PropertyHelper
from noora.system.Ora import Ora
from noora.io.File import File
from noora.connectors.MysqlConnector import MysqlConnector
from noora.connectors.ConnectionExecutor import ConnectionExecutor


class CreatePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "create", MysqlConnector())

    def execute(self, arguments, properties):
        properties.set_property('create.dir', os.path.join(properties.get_property('current.dir'), 'create'))

        host = arguments.h
        Fail.fail_on_no_host(host)

        default_databases = properties.get_property('databases')
        databases = Ora.nvl(arguments.d, default_databases)
        Fail.fail_on_invalid_database(arguments.d, properties)

        default_environment = properties.get_property('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        objects = properties.get_property('create_objects')

        alias = arguments.a
        database_aliases = properties.get_property('database_aliases')
        Fail.fail_on_invalid_alias(alias, properties)

        # if an alias is given, only this database will be installed, other databases will be ignored.
        if alias:
            print "using alias :" + alias
            databases = [alias]

        connector = self.get_connector()
        create_dir = properties.get_property('create.dir')

        for database in databases:
            print "creating database '" + database + "' on host '" + host + "' using environment '" + environment + "'"

            users = properties.get_property('mysql_users')
            username = PropertyHelper.get_mysql_user(users, host, database)
            password = PropertyHelper.get_mysql_passwd(users, host, database)

            executor = {}
            executor['host'] = host
            executor['database'] = database
            executor['username'] = username
            executor['password'] = password

            database_folder = PropertyHelper.get_database_folder(database, database_aliases)

            for object in objects:
                # global ddl objects

                folder = File(os.path.join(create_dir, database_folder, 'ddl', object))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(os.path.join(create_dir, database_folder, 'ddl', object, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(create_dir, database_folder, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(create_dir, database_folder, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print "database '" + database + "' created."
