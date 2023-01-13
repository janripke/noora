from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader

from noora.system.ClassLoader import ClassLoader

from noora.plugins.postgresql.PGSQLPlugin import PGSQLPlugin


class RecreatePlugin(PGSQLPlugin):
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
        target_version = arguments.get('version')

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
        Drop, create and update the database. Will loop over all versions and
        initialize the database to the latest version available.

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
        print(f"arguments: {arguments}")

        # find and execute the drop plugin.
        plugin = ClassLoader.load_class(ClassLoader.find_plugin(properties['technology'], 'drop'))
        plugin.execute(properties, arguments)

        # find and execute the create plugin.
        plugin = ClassLoader.load_class(ClassLoader.find_plugin(properties['technology'], 'create'))
        plugin.execute(properties, arguments)

        # find and execute the update plugin.
        plugin = ClassLoader.load_class(ClassLoader.find_plugin(properties['technology'], 'update'))
        # create the arguments and execute the plugin
        for version in prepared_args['update_versions']:
            arguments['version'] = version
            plugin.execute(properties, arguments)
