from noora.io.File import File
from noora.io.Files import Files
from noora.version.Version import Version


class VersionLoader(object):
    """
    Class providing functionality to determine all versions on the current
    project.
    """
    def __init__(self, versions):
        """
        Initialize the class.

        :param versions: A ``noora.version.Versions.Versions`` instance.
        """
        self.__versions = versions

    def load(self, properties):
        """
        Find all versions on the current project and add them to the list.

        :param properties: An instance of ``noora.system.Properties.Properties``.
        """
        alter = File(properties.get("alter.dir"))
        if alter.exists():
            files = Files()
            for version in files.list(alter):
                self.__versions.add(Version(version.tail()))

        create = File(properties.get("create.dir"))
        if create.exists():
            self.__versions.add(Version(properties.get("default_version")))
