#!/usr/bin/env python

import unittest

from noora.io.File import File
from noora.processor.PreProcessor import PreProcessor
from noora.shell.CallFactory import CallFactory
from noora.shell.Shell import Shell
from noora.system.Properties import Properties
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.VersionGuesser import VersionGuesser
from noora.version.Version import Version
import os


class TestVersion(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCheckVersion(self):

        properties = Properties()
        properties.set_property("current.dir", os.path.abspath('.'))
        properties.set_property('create.dir', os.path.join(properties.get_property('current.dir'), 'create'))
        properties.set_property('alter.dir', os.path.join(properties.get_property('current.dir'), 'alter'))
        properties.set_property('default_version', '1.0.0')

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        previous = versions.previous(Version('1.0.2'))
        self.assertEqual(previous.get_value(), '1.0.1', 'invalid version')

        previous = versions.previous(Version('1.0.1'))
        self.assertEqual(previous.get_value(), '1.0.0', 'invalid version')

        # this is the odd one. Given is the first version, because off the fact that there is no previous version,
        # the first version is returned.
        previous = versions.previous(Version('1.0.0'))
        self.assertEqual(previous.get_value(), '1.0.0', 'invalid version')


if __name__ == '__main__':
    unittest.main()
