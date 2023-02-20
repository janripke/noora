import os

from noora.system import ora
from noora.system import property_helper
from noora.io.file import File

from noora.plugins.mssql.mssql_plugin import MssqlPlugin
from noora.plugins.fails import Fail

from noora.connectors.connection_executor import ConnectionExecutor


class DropPlugin(MssqlPlugin):
    """Class providing functionality to drop (clear out) a database."""
    def _validate_and_prepare(self, properties, arguments):
        prepared_args = {}

        host = arguments.get('host')
        Fail.fail_on_no_host(host)
        Fail.fail_on_invalid_host(host, properties)
        Fail.fail_on_blocked_hosts(host, properties)
        prepared_args['host'] = host

        environment = arguments.get('environment')
        default_environment = properties.get('default_environment')
        environment = ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

        connection_string = arguments.get('connection_string')
        prepared_args['connection_string'] = property_helper.connection_credentials(connection_string)
        Fail.fail_on_host_mismatch(host, prepared_args['connection_string'])
        return prepared_args

    def execute(self, properties, arguments):
        """
        Drop a database after checking if schema and environment are
        valid values. Also check that host is not on the block list.

        :type properties: system.Properties.Properties
        :param properties: The project properties
        :type arguments: dict
        :param arguments: This dict contains the plugin arguments:

            * **host**: The hostname to drop on;
            * **environment**: Environment to drop the database from.
        """
        prepared_args = self._validate_and_prepare(properties, arguments)

        host = prepared_args['host']
        schemes = properties.get('schemes')
        environment = prepared_args['environment']
        database = properties.get('database')
        objects = properties.get('drop_objects')

        # retrieve the database connection credentials through
        # the commandline option --connection-string
        connection_string = prepared_args['connection_string']
        if connection_string:
            users = connection_string
        if not connection_string:
            # retrieve the user credentials for this database project.
            users = properties.get('mssql_users')

            # try to retrieve the users from the credentials file, when no users are configured in
            # myproject.json.
            if not users:
                # retrieve the name of this database project, introduced in version 1.0.12
                profile = property_helper.get_profile(properties)
                if profile:
                    users = profile.get('mssql_users')

        for schema in schemes:
            print("dropping schema '{schema}' in database '{db}' "
                  "on host '{host}' using environment '{env}'".format(
                    schema=schema, db=database, host=host, env=environment))

            executor = property_helper.get_mssql_properties(users, host, database, schema)
            executor['database'] = database

            connector = self.get_connector()

            for obj in objects:
                folder = File(os.path.join(properties.get('plugin.dir'), 'mssql', 'drop', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print("schema '{}' dropped.".format(schema))
