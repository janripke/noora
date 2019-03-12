import os

from noora.system import PropertyHelper
from noora.system import Ora
from noora.io.File import File

from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail

from noora.connectors.MssqlConnector import MssqlConnector
from noora.connectors.ConnectionExecutor import ConnectionExecutor


class CreatePlugin(Plugin):
    _connector = MssqlConnector

    def prepare(self, host, schema, environment):
        """
        Prepare database creation by checking if schema and environment are valid values.

        :param host: The hostname to create on
        :param schema: Schema to create
        :param environment: Environment to create the database in
        """
        properties = self._properties

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
        Create a new database instance for the latest version
        """
        properties = self._properties
        host = self.get_argument('host')
        schemes = self.get_argument('schemes')
        environment = self.get_argument('environment')

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

        connector = self.get_connector()
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
