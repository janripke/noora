import os

from noora.system import Ora
from noora.system import PropertyHelper
from noora.io.File import File

from noora.plugins.mssql.MssqlPlugin import MssqlPlugin
from noora.plugins.Fail import Fail

from noora.connectors.ConnectionExecutor import ConnectionExecutor


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
        environment = Ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

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

            executor = PropertyHelper.get_mssql_properties(users, host, database, schema)
            executor['database'] = database

            connector = self.get_connector()

            for obj in objects:
                folder = File(os.path.join(properties.get('plugin.dir'), 'mssql', 'drop', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print("schema '{}' dropped.".format(schema))
