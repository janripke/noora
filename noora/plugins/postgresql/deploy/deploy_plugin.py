import os
from noora.version.versions import Versions
from noora.version.version_loader import VersionLoader
from noora.exceptions.plugins.plugin_exception import PluginException
from noora.system.class_loader import ClassLoader
from noora.io.file import File
from noora.plugins.postgresql.pqsql_plugin import PGSQLPlugin
from noora.system import property_helper
from noora.system import ora
from noora.plugins.fails import Fail


def plan(installed_version: str, prepared_arguments: dict) -> dict:
    """
    Create a deployment plan.
    """
    create_version = prepared_arguments.get("default_version")
    update_versions = prepared_arguments.get("update_versions")

    # a fresh, first time deployment
    if not installed_version:
        return {
            "default_version": create_version,
            "update_versions": update_versions
        }

    # the create is installed but not any updates
    if installed_version == create_version:
        return {
            "default_version": None,
            "update_versions": update_versions
        }

    # an update is installed, find where to start from
    if installed_version in update_versions:
        return {
            "default_version": None,
            "update_versions": update_versions[update_versions.index(installed_version) + 1::]
        }


def fetch_installed_version(connector, executor, properties):
    plugin_dir = properties.get('plugin.dir')
    script = File(os.path.join(plugin_dir, 'postgresql', 'deploy', 'fetch_version.sql'))
    executor['script'] = script

    try:
        connector.execute(executor, properties)
        result = connector.get_result()
    except PluginException as e:
        result = ""
        if 'ERROR:  relation "application_properties" does not exist' not in e.__str__():
            raise e

    if result:
        result = result.replace('\r\n', '\n')
        result = result.replace('\r', '\n')
        result = result.split('\n')
        return result[1]


class DeployPlugin(PGSQLPlugin):
    """
    This class provides functionality to drop, create and update a database
    to a specified version.
    """
    def _validate_and_prepare(self, properties, arguments):
        """
        Prepare the version list here. All other preparation is handled by the
        plugins in the chain.
        """
        prepared_args = {
            'default_version': properties.get('default_version'),
            'update_versions': [],
        }

        host = arguments.get('host')
        Fail.fail_on_no_host(host)
        Fail.fail_on_invalid_host(host, properties)
        prepared_args['host'] = host

        environment = arguments.get('environment')
        default_environment = properties.get('default_environment')
        environment = ora.nvl(environment, default_environment)
        Fail.fail_on_invalid_environment(environment, properties)
        prepared_args['environment'] = environment

        prepared_args['connection_string'] = arguments.get('connection_string')

        target_version = arguments.get('version')

        if target_version:
            if target_version.lower() == "latest":
                target_version = None

        # If the target version is the default, we stop here because create takes care of this
        if prepared_args['default_version'] == target_version:
            return prepared_args

        # Here we determine the initial version
        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()

        # retrieve all versions
        for version in versions.list():
            # First add this version if it's not the default one, because that's handled by create
            if version.get_value() != prepared_args['default_version']:
                prepared_args['update_versions'].append(version.get_value())

            # Then, if we reached the target version, we break
            if version.get_value() == target_version:
                break

        return prepared_args

    def execute(self, properties, arguments):
        """
        Deploy the database. Retrieves the installed versions from the postgreSQL.
        Will loop over all versions that are not installed.

        :type properties: system.Properties.Properties
        :param properties: The project properties
        :type arguments: dict
        :param arguments: This dict contains the plugin arguments:

            * **version**: Desired target version;
            * **host**: Hostname to connect to;
            * **port**: Port to connect to (optional);
            * **environment**: Name of the environment (optional).
        """
        prepared_args = self._validate_and_prepare(properties, arguments)
        host = prepared_args['host']

        # retrieve the database connection credentials through
        # the commandline option --connection-string
        connection_string = prepared_args['connection_string']
        if connection_string:
            users = property_helper.connection_credentials(connection_string)

        if not connection_string:
            # retrieve the user credentials for this database project.
            users = properties.get('postgresql_users')

            # try to retrieve the users from the credentials file, when no users are configured in
            # myproject.json.
            if not users:
                # retrieve the name of this database project, introduced in version 1.0.12
                profile = property_helper.get_profile(properties)
                if profile:
                    users = profile.get('postgresql_users')

        connector = self.get_connector()
        version_database = properties.get('version_database')
        executor = property_helper.get_postgres_properties(users, host, version_database)
        installed_version = fetch_installed_version(connector, executor, properties)

        planned_versions = plan(installed_version, prepared_args)
        if planned_versions.get("default_version"):
            # find and execute the create plugin.
            plugin = ClassLoader.load_class(ClassLoader.find_plugin(properties['technology'], 'create'))
            plugin.execute(properties, arguments)

        # find and execute the update plugin.
        plugin = ClassLoader.load_class(ClassLoader.find_plugin(properties['technology'], 'update'))
        # create the arguments and execute the plugin
        for version in planned_versions.get("update_versions"):
            arguments['version'] = version
            plugin.execute(properties, arguments)

        # show that nothing happened, when
        if not planned_versions.get("default_version") and not planned_versions.get("update_versions"):
            print("Nothing to deploy")
