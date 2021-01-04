import os

from noora.system import PropertyHelper
from noora.system import Ora
from noora.io.File import File

from noora.plugins.mssql.MssqlPlugin import MssqlPlugin
from noora.plugins.Fail import Fail

from noora.connectors.ConnectionExecutor import ConnectionExecutor


class CreatePlugin(MssqlPlugin):
    """Plugin for creating (initializing) a MySQL database."""
    def _validate_and_prepare(self, properties, arguments):
        prepared_args = {}

        # Check host
        host = arguments.get('host')
        Fail.fail_on_no_host(host)
        Fail.fail_on_invalid_host(host, properties)
        prepared_args['host'] = host

        # Check environment
        environment = arguments.get('environment')
        default_environment = properties.get('default_environment')
        environment = Ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

        return prepared_args

    def execute(self, properties, arguments):
        """
        Create a new database instance for the initial version.

        :type properties: system.Properties.Properties
        :param properties: The project properties
        :type arguments: dict
        :param arguments: This dict contains the plugin arguments:

            * **host**: The hostname where the database is running;
            * **environment**: The environment to create the database in (optional).
        """
        prepared_args = self._validate_and_prepare(properties, arguments)

        host = prepared_args['host']
        schemes = properties.get('schemes')
        environment = prepared_args['environment']

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

            executor = PropertyHelper.get_mssql_properties(users, host, database, schema)
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
