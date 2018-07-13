from noora.io.File import File
from noora.io.Files import Files
from noora.version.Version import Version


class VersionLoader:
    def __init__(self, versions):
        self.__versions = versions

    def load(self, properties):
        alter = File(properties.get_property("alter.dir"))
        if alter.exists():
            files = Files()
            for version in files.list(alter):
                print "version", version.tail()
                self.__versions.add(Version(version.tail()))

        create = File(properties.get_property("create.dir"))
        if create.exists():
            self.__versions.add(Version(properties.get_property("default_version")))
