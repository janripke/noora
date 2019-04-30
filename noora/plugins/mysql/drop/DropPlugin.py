import os

from noora.system import PropertyHelper
from noora.system import Ora
from noora.io.File import File

from noora.plugins.mysql.MysqlPlugin import MysqlPlugin
from noora.plugins.Fail import Fail

from noora.connectors.ConnectionExecutor import ConnectionExecutor


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
        environment = Ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

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
            databases = Ora.nvl(database, default_databases)
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

        # retrieve the user credentials for this database project.
        users = properties.get('mysql_users')

        # try to retrieve the users from the credentials file, when no users are configured in
        # myproject.json.
        if not users:
            # retrieve the name of this database project, introduced in version 1.0.12
            profile = PropertyHelper.get_profile(properties)
            if profile:
                users = profile.get('mysql_users')

        # fail when no users are found. This means that they are not set in myproject.json or
        # credentials.json
        Fail.fail_on_no_users(users)

        for database in databases:
            print("dropping database '{db}' on host '{host}' using environment '{env}'".format(
                db=database, host=host, env=environment))

            executor = PropertyHelper.get_mysql_properties(users, host, database)

            connector = self.get_connector()

            for obj in objects:
                folder = File(os.path.join(properties.get('plugin.dir'), 'mysql', 'drop', obj))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print("database '{}' dropped".format(database))
