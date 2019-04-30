import os

from noora.version.Version import Version


class VersionGuesser(object):
    """Utilities for inspecting current version of a project"""
    def __init__(self, properties, versions):
        """
        Initialize the class.

        :param properties: An initialized properties object;
        :param versions: The list of versions for the project.
        """
        self.__properties = properties
        self.__versions = versions

    def guess(self, version=None):
        """
        Do some guessing based on the current version.

        :param version (optional): if provided, find the version in the list.
            If not provided, find the next version on the project;
        :return: The current (if found) or next version, or the default
            version if all else fails.
        """
        versions = self.__versions
        properties = self.__properties
        if version:
            return Version(version)
        if versions.next():
            return versions.next()
        return Version(properties.get("default_version"))

    def to_folder(self, version):
        properties = self.__properties
        if version == properties.get("default_version"):
            return properties.get("create.dir")
        return os.path.join(properties.get("alter.dir"), version)
