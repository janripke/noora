import os
from noora.version.Version import Version


class VersionGuesser:
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
        return Version(properties.get_property("default_version"))

    def to_folder(self, version):
        properties = self.__properties
        if version == properties.get_property("default_version"):
            return properties.get_property("create.dir")
        return os.path.join(properties.get_property("alter.dir"), version)
