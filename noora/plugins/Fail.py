import six

from noora.exceptions.plugins.PluginException import PluginException
from noora.exceptions.plugins.BlockedHostException import BlockedHostException
from noora.exceptions.plugins.UnknownVersionException import UnknownVersionException

from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.Version import Version


class Fail(object):
    @staticmethod
    def fail_on_no_host(host):
        if not host:
            raise PluginException("no host was given")
        elif not issubclass(type(host), six.string_types):
            raise PluginException("provided host is not a string")

    @staticmethod
    def fail_on_no_port(port):
        if not port:
            raise PluginException("no port was provided")
        elif type(port) is not int:
            raise PluginException("provided port is not an integer")

    @staticmethod
    def fail_on_no_version(version):
        if not version:
            raise PluginException("no version was given")
        elif not issubclass(type(version), six.string_types):
            raise PluginException("version is not a string")

    @staticmethod
    def fail_on_no_users(users):
        if not users:
            raise PluginException("no users found")
        elif type(users) is not list:
            raise PluginException("provided users is not a list")

    @staticmethod
    def fail_on_no_schema(schema):
        if not schema:
            raise PluginException("no schema name provided")
        elif not issubclass(type(schema), six.string_types):
            raise PluginException("provided schema is not a string")

    @staticmethod
    def fail_on_no_database(database):
        if not database:
            raise PluginException("no database name provided")
        elif not issubclass(type(database), six.string_types):
            raise PluginException("provided database is not a string")

    @staticmethod
    def fail_on_no_user(user):
        if not user:
            raise PluginException("no username provided")
        elif not issubclass(type(user), six.string_types):
            raise PluginException("provided username is not a string")

    @staticmethod
    def fail_on_invalid_database(database, properties):
        if database and database not in properties.get('databases'):
            raise PluginException("database '{}' is not valid for this project".format(database))

    @staticmethod
    def fail_on_invalid_schema(schema, properties):
        if schema and schema not in properties.get('schemes'):
            raise PluginException("schema '{}' is not valid for this project".format(schema))

    @staticmethod
    def fail_on_invalid_environment(environment, properties):
        if environment and environment not in properties.get('environments'):
            raise PluginException(
                "environment '{}' is not valid for this project".format(environment))

    @staticmethod
    def fail_on_invalid_alias(alias, properties):
        if alias and alias not in properties.get('aliasses'):
            raise PluginException("alias '{}' is not valid for this project".format(alias))

    @staticmethod
    def fail_on_unknown_version(version, properties):
        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()

        if not versions.exists(Version(version)):
            raise UnknownVersionException(
                "version {} is not valid for this project".format(version))

    @staticmethod
    def fail_on_blocked_hosts(host, properties):
        blocked_hosts = properties.get('blocked_hosts')
        if host in blocked_hosts:
            raise BlockedHostException("blocked host: {}".format(host))

    @staticmethod
    def fail_on_invalid_host(host, properties):
        """
        Verify that host is in host_list and raise an exception if not.

        :param host: The host to look up
        :param host_list: Properties containing the host list
        """
        host_list = properties.get('{}_hosts'.format(properties.get('technology')))
        if host not in host_list:
            raise PluginException(
                "Host {} not in list of valid hosts for this project".format(host))
