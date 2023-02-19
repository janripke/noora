import os

from noora.system import property_helper
from noora.system import ora
from noora.io.file import File

from noora.plugins.mysql.mysql_plugin import MysqlPlugin
from noora.plugins.fails import Fail

from noora.connectors.connection_executor import ConnectionExecutor


class DropPlugin(MysqlPlugin):
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

        alias = arguments.get('alias')
        Fail.fail_on_invalid_alias(alias, properties)
        # if an alias is given, only this database will be installed, other databases will be
        # ignored.
        if alias:
            print("using alias: {}".format(alias))
            prepared_args['databases'] = [alias]
        else:
            database = arguments.get('database')
            Fail.fail_on_invalid_database(database, properties)
            default_databases = properties.get('databases')
            databases = ora.nvl(database, default_databases)
            prepared_args['databases'] = databases

        return prepared_args

    def execute(self, properties, arguments):
        """
        Drop a database after checking if schema and environment are
        valid values. Also check that host is not on the block list.

        :type properties: system.Properties.Properties
        :param properties: The project properties
        :type arguments: dict
        :param arguments: This dict contains the plugin arguments:

            * **host**: The hostname where the database will run;
            * **database**: The database to create in (optional);
            * **environment** (optional): The environment to create the database in;
            * **alias** (optional): The database alias. If provided, this will overrule the database argument.
        """
        prepared_args = self._validate_and_prepare(properties, arguments)

        host = prepared_args['host']
        environment = prepared_args['environment']
        databases = prepared_args['databases']

        objects = properties.get('drop_objects')

        # retrieve the database connection credentials through
        # the commandline option --connection-string
        connection_string = prepared_args['connection_string']
        if connection_string:
            users = connection_string
        if not connection_string:
            # retrieve the user credentials for this database project.
            users = properties.get('mysql_users')

            # try to retrieve the users from the credentials file, when no users are configured in
            # myproject.json.
            if not users:
                # retrieve the name of this database project, introduced in version 1.0.12
                profile = property_helper.get_profile(properties)
                if profile:
                    users = profile.get('mysql_users')

        # fail when no users are found. This means that they are not set in myproject.json or
        # credentials.json
        Fail.fail_on_no_users(users)

        for database in databases:
            print("dropping database '{db}' on host '{host}' using environment '{env}'".format(
                db=database, host=host, env=environment))

            executor = property_helper.get_mysql_properties(users, host, database)

            connector = self.get_connector()

            for obj in objects:
                folder = File(os.path.join(properties.get('plugin.dir'), 'mysql', 'drop', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print("database '{}' dropped".format(database))
