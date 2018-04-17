from noora.plugins.PluginException import PluginException
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.Version import Version

class Fail:
    def __init__(self):
        pass

    @staticmethod
    def fail_on_no_host(host):
        if not host:
            message = "no host was given"
            raise PluginException(message)

    @staticmethod
    def fail_on_no_version(version):
        if not version:
            message = "no version was given"
            raise PluginException(message)

    @staticmethod
    def fail_on_no_command(commands):
        if not commands:
            message = "no command was given"
            raise PluginException(message)

    @staticmethod
    def fail_on_invalid_plugin(plugin):
        if not plugin:
            message = "the given plugin is not valid for this project"
            raise PluginException(message)

    @staticmethod
    def fail_on_invalid_database(database, properties):
        if database:
            databases = properties.get_property('databases')
            if database not in databases:
                message = "the given database is not valid for this project"
                raise PluginException(message)

    @staticmethod
    def fail_on_invalid_schema(schema, properties):
        if schema:
            schemes = properties.get_property('schemes')
            if schema not in schemes:
                message = "the given schema is not valid for this project"
                raise PluginException(message)

    @staticmethod
    def fail_on_invalid_environment(environment, properties):
        if environment:
            environments = properties.get_property('environments')
            if environment not in environments:
                message = "the given environment is not valid for this project"
                raise PluginException(message)

    @staticmethod
    def fail_on_invalid_alias(alias, properties):
        if alias:
            aliasses = properties.get_property('aliasses')
            if alias not in aliasses:
                message = "the given alias is not valid for this project"
                raise PluginException(message)

    @staticmethod
    def fail_on_unknown_version(version, properties):
        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()

        if not versions.exists(Version(version)):
            message = "the given version is not valid for this project"
            raise PluginException(message)
