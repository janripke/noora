#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"
EXAMPLE_DIR = NOORA_DIR + os.sep + 'examples'
PROJECT_DIR = EXAMPLE_DIR + os.sep + 'project-db'


sys.path.append(NOORA_DIR)
import core.ParameterHelper as ParameterHelper
import core.NooraException  as NooraException
import core.Config          as Config


class TestConfig(unittest.TestCase):

    def getParameterHelper(self):
        parameterHelper = ParameterHelper.ParameterHelper()
        return parameterHelper

    def getConfigObject(self):
        configObject = Config.Config(PROJECT_DIR)
        return configObject

    def setUp(self):
        self.setPluginClass("static.drop.DropPlugin.DropPlugin")

    def tearDown(self):
        pass

    def testConfig(self):
        config = self.getConfigObject()


if __name__ == '__main__':
    unittest.main()
