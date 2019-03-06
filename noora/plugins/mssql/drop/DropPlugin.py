import os

from noora.system import Ora
from noora.system import PropertyHelper
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
            raise BlockedHostException("block host: {}".format(host))

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
            print("dropping schema '{schema}' in database '{db}' "
                  "on host '{host}' using environment '{env}'".format(
                    schema=schema, db=database, host=host, env=environment))

            executor = PropertyHelper.get_mssql_properties(users, host, schema)
            executor['database'] = database

            connector = self.get_connector()

            for obj in objects:
                folder = File(os.path.join(self.get_drop_dir(properties), obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print("schema '{}' dropped.".format(schema))
