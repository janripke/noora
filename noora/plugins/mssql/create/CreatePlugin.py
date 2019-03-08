import os

import click

from noora.system.Properties import properties
from noora.system import PropertyHelper
from noora.system import Ora
from noora.io.File import File

from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail

from noora.connectors.MssqlConnector import MssqlConnector
from noora.connectors.ConnectionExecutor import ConnectionExecutor


class CreatePlugin(Plugin):
    _connector = MssqlConnector

    @staticmethod
    @click.command()
    @click.option('-h', '--host', required=True, prompt=True, default='localhost')
    @click.option('-s', '--schema', required=False, prompt='Schema name')
    @click.option('-s', '--environment', required=False, prompt='Environment')
    def execute(host, schema, environment):
        """
        Create a new database instance for the latest version
        """
        properties['create.dir'] = os.path.join(properties.get('current.dir'), 'create')

        Fail.fail_on_no_host(host)

        default_schemes = properties.get('schemes')
        schemes = Ora.nvl(schema, default_schemes)
        Fail.fail_on_invalid_schema(schema, properties)

        default_environment = properties.get('default_environment')
        environment = Ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)

        database = properties.get('database')
        objects = properties.get('create_objects')

        # retrieve the user credentials for this database project.
        users = properties.get('mssql_users')

        # try to retrieve the users from the credentials file, when no users are configured in
        # myproject.json.
        if not users:
            # retrieve the name of this database project, introduced in version 1.0.12
            profile = PropertyHelper.get_profile(properties)
            if profile:
                users = profile.get('mssql_users')

        connector = CreatePlugin.get_connector()
        create_dir = properties.get('create.dir')
        for schema in schemes:
            print("creating schema '{schema}' in database '{db}' "
                  "on host '{host}' using environment '{env}'".format(
                    schema=schema, db=database, host=host, env=environment))

            executor = PropertyHelper.get_mssql_properties(users, host, schema)
            executor['database'] = database

            for obj in objects:
                # global ddl objects
                folder = File(os.path.join(create_dir, schema, 'ddl', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(os.path.join(create_dir, schema, 'ddl', obj, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(create_dir, schema, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(create_dir, schema, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print("schema '{}' created.".format(schema))
