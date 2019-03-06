from noora.exceptions.PluginException import PluginException
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.Version import Version


class Fail(object):
    @staticmethod
    def fail_on_no_host(host):
        if not host:
            raise PluginException("no host was given")

    @staticmethod
    def fail_on_no_version(version):
        if not version:
            raise PluginException("no version was given")

    @staticmethod
    def fail_on_no_command(commands):
        if not commands:
            raise PluginException("no command was given")

    @staticmethod
    def fail_on_no_users(users):
        if not users:
            raise PluginException("no users found")

    @staticmethod
    def fail_on_invalid_plugin(plugin):
        if not plugin:
            raise PluginException("the given plugin is not valid for this project")

    @staticmethod
    def fail_on_invalid_database(database, properties):
        if database:
            databases = properties.get('databases')
            if database not in databases:
                raise PluginException("the given database is not valid for this project")

    @staticmethod
    def fail_on_invalid_schema(schema, properties):
        if schema:
            schemes = properties.get('schemes')
            if schema not in schemes:
                raise PluginException("the given schema is not valid for this project")

    @staticmethod
    def fail_on_invalid_environment(environment, properties):
        if environment:
            environments = properties.get('environments')
            if environment not in environments:
                raise PluginException("the given environment is not valid for this project")

    @staticmethod
    def fail_on_invalid_alias(alias, properties):
        if alias:
            aliasses = properties.get('aliasses')
            if alias not in aliasses:
                raise PluginException("the given alias is not valid for this project")

    @staticmethod
    def fail_on_unknown_version(version, properties):
        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()

        if not versions.exists(Version(version)):
            raise PluginException("the given version is not valid for this project")
