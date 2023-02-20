#!/usr/bin/env python

import unittest
from noora.version.versions import Versions
from noora.version.version_loader import VersionLoader
from noora.version.version import Version
import os


class TestVersion(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCheckVersion(self):

        properties = dict()
        properties["current.dir"] = os.path.abspath('.')
        properties['create.dir'] = os.path.join(properties.get('current.dir'), 'create')
        properties['alter.dir'] = os.path.join(properties.get('current.dir'), 'alter')
        properties['default_version'] = '1.0.0'

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
