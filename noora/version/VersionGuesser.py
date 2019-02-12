import os

from noora.version.Version import Version


class VersionGuesser(object):
    def __init__(self, properties, versions):
        self.__properties = properties
        self.__versions = versions

    def guess(self, version):
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
