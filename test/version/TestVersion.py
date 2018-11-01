#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from src.org.noora.version.Versions import Versions

from src.org.noora.io.Properties import Properties
from src.org.noora.io.PropertyLoader import PropertyLoader
from src.org.noora.io.File import File
from src.org.noora.io.FileReader import FileReader
from src.org.noora.io.Path import Path

from src.org.noora.version.Version import Version
from src.org.noora.version.VersionLoader import VersionLoader


class VersionGuesser():
    def __init__(self, properties, versions):
        self.__properties = properties
        self.__versions = versions

    def __next__(self, last):
        last

    def guess(self, version):
        versions = self.__versions
        properties = self.__properties
        if version:
            return Version(version)
        if versions.next():
            return versions.next()
        return Version(properties.getPropertyValue("DEFAULT_VERSION"))

    def toFolder(self, version):
        properties = self.__properties
        if version == properties.getPropertyValue("DEFAULT_VERSION"):
            return properties.getPropertyValue("create.dir")
        return Path.path(properties.getPropertyValue("alter.dir"), version)


class TestBase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testVersionLoader(self):

        properties = Properties()
        propertyLoader = PropertyLoader(properties)

        file = File("myproject.conf")
        fileReader = FileReader(file)
        propertyLoader.load(fileReader)

        properties.setProperty("current.dir", os.path.abspath('.'))
        properties.setProperty("project.file", "myproject.conf")
        properties.setProperty("alter.dir", Path.path(properties.getPropertyValue("current.dir"), "alter"))
        properties.setProperty("create.dir", Path.path(properties.getPropertyValue("current.dir"), "create"))
        print("current.dir", properties.getPropertyValue("current.dir"))
        # print "alter.dir",properties.getPropertyValue("alter.dir")
        # print "default_version :" + properties.getPropertyValues("DEFAULT_VERSION")

        # a File object is not a Version object
        #
        versions = Versions()
        versionLoader = VersionLoader(versions)
        versionLoader.load(properties)
        versions.sort()
        # versions.sort()
        # print "versions",versions.getVersions()
        v = Version('1.0.1')
        print(versions.previous(v).getValue())

        print(versions.last().toString())
        print(versions.next().toString())

        versionGuesser = VersionGuesser(properties, versions)
        nextVersion = versionGuesser.guess(None).toString()
        print(versionGuesser.toFolder(nextVersion))

        # versioning is subject of study, so the are several methods of versioning used.
        # this means that there is some level abstraction present.
        # the abstraction level present requires to implement a specific method or choice.
        # i will study this on a later moment, for now it would be a good idea to create a class which
        # implements a specific versioning system, which is acknowledged or not.

        # it took me about 7 days to even start programming. In respect to previous sentences this actually means
        # that i felt that there were different approaches.
        # the link http://en.wikipedia.org/wiki/Software_versioning learned me that there are different approaches.
        # in order to achieve a robust versioning system for Noora, more research is required.

        # for python, it would be nice that i build a system which implements all the acknowledged version systems.
        # on the other hand, with the Noora approach in mind, the implementation of Mayor,Minor,Revision,Patch system
        # would be, for now, the best approach.

        # versions=[]
        # alterFolder=projectHelper.getAlterFolder()
        # if projectHelper.folderPresent(alterFolder):
        #  versions=projectHelper.findFolders(alterFolder)
        # createFolder=projectHelper.getCreateFolder()
        # if projectHelper.folderPresent(createFolder):
        #  versions.append(defaultVersion)

        # versionHelper=VersionHelper.VersionHelper(versions)
        # versions=versionHelper.sort()
        # versions.sort()
        # return versions

    def versions(self):
        versions = Versions()
        v = Version(1, 0, 0)
        versions.add(v)
        v = Version(10, 0, 0)
        versions.add(v)
        v = Version(2, 0, 0)
        versions.add(v)
        v = Version(10, 0, 0, 1)
        versions.add(v)

        versions.sort()
        for version in versions.getVersions():
            print()
            version.getMajor(), version.getMinor(), version.getRevision(), version.getPatch()

    def versionListPass(self):
        v = [[2, 10, 0], [2, 7, 2, 4], [2, 8, 0], [2, 8, 0, 1], [2, 8, 0, 2], [2, 9, 0]]
        v.sort()
        print()
        v[0]

    def versionPass(self):

        v = [[1, 0, 1], [1, 0, 0, 1], [1, 0, 0, 10], [1, 0, 0, 2]]
        v.sort()
        # print v
        # vh = VersionHelper(v)
        # l = vh.sort()
        # return l

        v = [(1, 0, 1, None), (1, 0, 0, 1), (1, 0, 0, 10), (1, 0, 0, 2)]
        # print v
        v.sort()
        print()
        v

        versions = Versions()
        versions.addVersion(1, 0, 1)
        versions.addVersion(1, 0, 0, 1)
        versions.addVersion(1, 0, 0, 10)
        versions.addVersion(1, 0, 0, 2)
        versions.sort()

        vl = versions.getVersions()
        for version in vl:
            print()
            version.list()

        v = Version(1, 0, 0, 10)
        pv = versions.previousVersion(v)
        if pv: print()
        pv.list()
        lv = versions.lastVersion()
        if lv: print()
        lv.list()
        # versions.addVersion(1, 0, 0, 1)
        # versions.addVersion(1, 0, 0, 10)
        # versions.addVersion(1, 0, 0, 2)
        # versions.sort()
        # print versions.lastVersion().list()
        # print versions.getVersions()


if __name__ == '__main__':
    unittest.main()
