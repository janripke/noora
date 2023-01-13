import six

from noora.exceptions.plugins.PluginException import PluginException
from noora.exceptions.plugins.BlockedHostException import BlockedHostException
from noora.exceptions.plugins.UnknownVersionException import UnknownVersionException

from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.Version import Version


class Fail(object):
    """
    Class providing assertion methods for various attributes.
    PluginExceptions will be raised when an assertion fails.
    """
    @staticmethod
    def fail_on_no_host(host):
        """Verify that ``host`` is a string"""
        if not host:
            raise PluginException("no host was given")
        elif not issubclass(type(host), six.string_types):
            raise PluginException("provided host is not a string")

    @staticmethod
    def fail_on_no_port(port):
        """Verify that ``port`` is an integer"""
        if not port:
            raise PluginException("no port was provided")
        elif type(port) is not int:
            raise PluginException("provided port is not an integer")

    @staticmethod
    def fail_on_no_version(version):
        """Verify that ``version`` is a string"""
        if not version:
            raise PluginException("no version was given")
        elif not issubclass(type(version), six.string_types):
            raise PluginException("version is not a string")

    @staticmethod
    def fail_on_no_users(users):
        """Verify that ``users`` is a list"""
        if not users:
            raise PluginException("no users found")
        elif type(users) is not list:
            raise PluginException("provided users is not a list")

    @staticmethod
    def fail_on_no_schema(schema):
        """Verify that ``schema`` is a string"""
        if not schema:
            raise PluginException("no schema name provided")
        elif not issubclass(type(schema), six.string_types):
            raise PluginException("provided schema is not a string")

    @staticmethod
    def fail_on_no_database(database):
        """Verify that ``database`` is a string"""
        if not database:
            raise PluginException("no database name provided")
        elif not issubclass(type(database), six.string_types):
            raise PluginException("provided database is not a string")

    @staticmethod
    def fail_on_no_user(user):
        """Verify that ``user`` is a string"""
        if not user:
            raise PluginException("no username provided")
        elif not issubclass(type(user), six.string_types):
            raise PluginException("provided username is not a string")

    @staticmethod
    def fail_on_invalid_database(database, properties):
        """Verify that ``database`` is valid for this project"""
        if database and database not in properties.get('databases'):
            raise PluginException("database '{}' is not valid for this project".format(database))

    @staticmethod
    def fail_on_invalid_schema(schema, properties):
        """Verify that ``schema`` is valid for this project"""
        if schema and schema not in properties.get('schemes'):
            raise PluginException("schema '{}' is not valid for this project".format(schema))

    @staticmethod
    def fail_on_invalid_environment(environment, properties):
        """Verify that ``environment`` is valid for this project"""
        if environment and environment not in properties.get('environments'):
            raise PluginException(
                "environment '{}' is not valid for this project".format(environment))

    @staticmethod
    def fail_on_invalid_alias(alias, properties):
        """Verify that ``alias`` is valid for this project"""
        if alias and alias not in properties.get('aliasses'):
            raise PluginException("alias '{}' is not valid for this project".format(alias))

    @staticmethod
    def fail_on_unknown_version(version, properties):
        """Verify that ``version`` is valid for this project"""
        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()

        if not versions.exists(Version(version)):
            raise UnknownVersionException(
                "version {} is not valid for this project".format(version))

    @staticmethod
    def fail_on_blocked_hosts(host, properties):
        """Make sure that ``host`` is not in the list of blocked hosts"""
        blocked_hosts = properties.get('blocked_hosts')
        if blocked_hosts:
            if host in blocked_hosts:
                raise BlockedHostException("blocked host: {}".format(host))

    @staticmethod
    def fail_on_invalid_host(host, properties):
        """
        Verify that host is in the host list for this project

        :param host: The host to look up
        :param host_list: Properties containing the host list
        """
        host_list = properties.get('{}_hosts'.format(properties.get('technology')))
        if host_list:
            if host not in host_list:
                raise PluginException(
                    "Host {} not in list of valid hosts for this project".format(host))
