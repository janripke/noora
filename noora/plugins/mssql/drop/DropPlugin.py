import os

from noora.system.Ora import Ora
from noora.system.PropertyHelper import PropertyHelper
from noora.io.File import File

from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.exceptions.BlockedHostException import BlockedHostException

from noora.connectors.ConnectionExecutor import ConnectionExecutor
from noora.connectors.MssqlConnector import MssqlConnector


class DropPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "drop", MssqlConnector())

    def parse_args(self, parser, args):
        parser.add_argument('-h', type=str, help='host', required=True)
        parser.add_argument('-s', type=str, help='schema', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        return parser.parse_args(args)

    def get_drop_dir(self, properties):
        return os.path.join(properties.get('plugin.dir'), 'mssql', 'drop')

    def fail_on_blocked_hosts(self, host, properties):
        blocked_hosts = properties.get('blocked_hosts')
        if host in blocked_hosts:
            message = "block host " + host
            raise BlockedHostException(message)

    def execute(self, arguments, properties):
        host = arguments.h
        Fail.fail_on_no_host(host)
        self.fail_on_blocked_hosts(host, properties)

        default_schemes = properties.get('schemes')
        schemes = Ora.nvl(arguments.s, default_schemes)
        Fail.fail_on_invalid_schema(arguments.s, properties)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        database = properties.get('database')
        objects = properties.get('drop_objects')

        # retrieve the user credentials for this database project.
        users = properties.get('mssql_users')

        # try to retrieve the users from the credentials file, when no users are configured in
        # myproject.json.
        if not users:
            # retrieve the name of this database project, introduced in version 1.0.12
            profile = PropertyHelper.get_profile(properties)
            if profile:
                users = profile.get('mssql_users')

        for schema in schemes:
            # FIXME: use format
            print("dropping schema '" + schema +
                  "' in database '" + database +
                  "' on host '" + host +
                  "' using environment '" + environment + "'")

            username = PropertyHelper.get_mssql_user(users, host, schema)
            password = PropertyHelper.get_mssql_password(users, host, schema)

            connector = self.get_connector()

            executor = {
                'host': host,
                'database': database,
                'schema':  schema,
                'username': username,
                'password': password,
            }

            for obj in objects:
                folder = File(os.path.join(self.get_drop_dir(properties), obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print("schema '" + schema + "' dropped.")
