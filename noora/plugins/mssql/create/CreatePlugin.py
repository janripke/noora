import os
from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.system.PropertyHelper import PropertyHelper
from noora.system.Ora import Ora
from noora.io.File import File
from noora.connectors.MssqlConnector import MssqlConnector
from noora.connectors.ConnectionExecutor import ConnectionExecutor


class CreatePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "create", MssqlConnector())

    def parse_args(self, parser, args):
        parser.add_argument('-h', type=str, help='host', required=True)
        parser.add_argument('-s', type=str, help='schema', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        return parser.parse_args(args)

    def execute(self, arguments, properties):
        properties['create.dir'] = os.path.join(properties.get('current.dir'), 'create')

        host = arguments.h
        Fail.fail_on_no_host(host)

        default_schemes = properties.get('schemes')
        schemes = Ora.nvl(arguments.s, default_schemes)
        Fail.fail_on_invalid_schema(arguments.s, properties)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        database = properties.get('database')
        objects = properties.get('create_objects')

        # retrieve the user credentials for this database project.
        users = properties.get('mssql_users')

        # try to retrieve the users from the credentials file, when no users are configured in myproject.json.
        if not users:
            # retrieve the name of this database project, introduced in version 1.0.12
            profile = PropertyHelper.get_profile(properties)
            if profile:
                users = profile.get('mssql_users')

        connector = self.get_connector()
        create_dir = properties.get('create.dir')
        for schema in schemes:
            print("creating schema '" + schema + "' in database '" + database + "' on host '" + host + "' using environment '" + environment + "'")

            username = PropertyHelper.get_mssql_user(users, host, schema)
            password = PropertyHelper.get_mssql_password(users, host, schema)

            executor = dict()
            executor['host'] = host
            executor['database'] = database
            executor['username'] = username
            executor['password'] = password

            # database_folder = PropertyHelper.get_database_folder(database, database_aliases)

            for object in objects:
                # global ddl objects

                folder = File(os.path.join(create_dir, schema, 'ddl', object))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(os.path.join(create_dir, schema, 'ddl', object, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(create_dir, schema, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(create_dir, schema, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print("schema '" + schema + "' created.")
