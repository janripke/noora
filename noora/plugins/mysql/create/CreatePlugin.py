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
        properties['create.dir'] = os.path.join(properties.get('current.dir'), 'create')

        host = arguments.h
        Fail.fail_on_no_host(host)

        default_databases = properties.get('databases')
        databases = Ora.nvl(arguments.d, default_databases)
        Fail.fail_on_invalid_database(arguments.d, properties)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        objects = properties.get('create_objects')

        alias = arguments.a
        database_aliases = properties.get('database_aliases')
        Fail.fail_on_invalid_alias(alias, properties)

        # if an alias is given, only this database will be installed, other databases will be ignored.
        if alias:
            print "using alias :" + alias
            databases = [alias]

        # retrieve the user credentials for this database project.
        users = properties.get('mysql_users')

        # try to retrieve the users from the credentials file, when no users are configured in myproject.json.
        if not users:
            # retrieve the name of this database project, introduced in version 1.0.12
            profile = PropertyHelper.get_profile(properties)
            if profile:
                users = profile.get('mysql_users')

        connector = self.get_connector()
        create_dir = properties.get('create.dir')

        for database in databases:
            print "creating database '" + database + "' on host '" + host + "' using environment '" + environment + "'"

            username = PropertyHelper.get_mysql_user(users, host, database)
            password = PropertyHelper.get_mysql_passwd(users, host, database)

            executor = dict()
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
