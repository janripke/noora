import os

from noora.system import PropertyHelper
from noora.system import Ora
from noora.io.File import File

from noora.plugins.postgresql.PGSQLPlugin import PGSQLPlugin
from noora.plugins.Fail import Fail

from noora.connectors.ConnectionExecutor import ConnectionExecutor


class CreatePlugin(PGSQLPlugin):
    """Plugin for creating (initializing) a PostgreSQL database."""
    def _validate_and_prepare(self, properties, arguments):
        prepared_args = {}

        host = arguments.get('host')
        Fail.fail_on_no_host(host)
        Fail.fail_on_invalid_host(host, properties)
        prepared_args['host'] = host

        environment = arguments.get('environment')
        default_environment = properties.get('default_environment')
        environment = Ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

        prepared_args['connection_string'] = arguments.get('connection_string')

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
        environment = prepared_args['environment']
        databases = properties.get('databases')

        objects = properties.get('create_objects')

        # retrieve the database connection credentials through
        # the commandline option --connection-string
        connection_string = prepared_args['connection_string']
        if connection_string:
            users = PropertyHelper.connection_credentials(connection_string)

        if not connection_string:
            # retrieve the user credentials for this database project.
            users = properties.get('postgresql_users')

            # try to retrieve the users from the credentials file, when no users are configured in
            # myproject.json.
            if not users:
                # retrieve the name of this database project, introduced in version 1.0.12
                profile = PropertyHelper.get_profile(properties)
                if profile:
                    users = profile.get('postgresql_users')

        # fail when no users are found. This means that they are not set in myproject.json or
        # credentials.json
        Fail.fail_on_no_users(users)

        connector = self.get_connector()
        create_dir = properties.get('create.dir')

        for database in databases:
            print("creating database '{db}' on host '{host}' using environment '{env}'".format(
                db=database, host=host, env=environment))

            executor = PropertyHelper.get_postgres_properties(users, host, database)

            for obj in objects:
                # global ddl objects
                folder = File(os.path.join(create_dir, database, 'ddl', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

                # environment specific ddl objects
                folder = File(os.path.join(create_dir, database, 'ddl', obj, environment))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            # global dat objects
            folder = File(os.path.join(create_dir, database, 'dat'))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            # environment specific dat objects
            folder = File(os.path.join(create_dir, database, 'dat', environment))
            ConnectionExecutor.execute(connector, executor, properties, folder)

            print("database '{}' created.".format(database))
