import os

import click

from noora.system.Properties import properties
from noora.system import Ora
from noora.system import PropertyHelper
from noora.io.File import File

from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.exceptions.BlockedHostException import BlockedHostException

from noora.connectors.ConnectionExecutor import ConnectionExecutor
from noora.connectors.MssqlConnector import MssqlConnector


class DropPlugin(Plugin):
    _connector = MssqlConnector

    @staticmethod
    def fail_on_blocked_hosts(host):
        blocked_hosts = properties.get('blocked_hosts')
        if host in blocked_hosts:
            raise BlockedHostException("block host: {}".format(host))

    @staticmethod
    @click.command()
    @click.option('-h', '--host', required=True, prompt=True, default='localhost')
    @click.option('-s', '--schema', required=False, prompt='Schema name')
    @click.option('-s', '--environment', required=False, prompt='Environment')
    def execute(host, schema, environment):
        """
        Drop a schema in the database for the specified environment
        """
        Fail.fail_on_no_host(host)
        DropPlugin.fail_on_blocked_hosts(host)

        default_schemes = properties.get('schemes')
        schemes = Ora.nvl(schema, default_schemes)
        Fail.fail_on_invalid_schema(schema, properties)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(schema, default_environment)
        Fail.fail_on_invalid_environment(schema, properties)

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
            print("dropping schema '{schema}' in database '{db}' "
                  "on host '{host}' using environment '{env}'".format(
                    schema=schema, db=database, host=host, env=environment))

            executor = PropertyHelper.get_mssql_properties(users, host, schema)
            executor['database'] = database

            connector = DropPlugin.get_connector()

            for obj in objects:
                folder = File(os.path.join(properties.get('plugin.dir'), 'mssql', 'drop', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print("schema '{}' dropped.".format(schema))
