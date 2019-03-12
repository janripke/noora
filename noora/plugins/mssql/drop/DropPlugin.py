import os

import click

from noora.system import Ora
from noora.system import PropertyHelper
from noora.io.File import File

from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail

from noora.connectors.ConnectionExecutor import ConnectionExecutor


class DropPlugin(Plugin):
    def prepare(self, host, schema, environment):
        """
        Prepare to drop database by checking if schema and environment are
        valid values. Also check that host is not on the block list

        :param host: The hostname to drop on
        :param schema: Schema to drop
        :param environment: Environment to drop the database from
        """
        properties = self._properties

        Fail.fail_on_blocked_hosts(host, properties)
        self.set_argument('host', host)

        default_schemes = properties.get('schemes')
        schemes = Ora.nvl(schema, default_schemes)
        Fail.fail_on_invalid_schema(schema, properties)
        self.set_argument('schemes', schemes)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        self.set_argument('environment', environment)

    def execute(self):
        """
        Drop a schema in the database for the specified environment
        """
        properties = self._properties
        host = self.get_argument('host')
        schemes = self.get_argument('schemes')
        environment = self.get_argument('environment')
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
