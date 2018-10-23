#!/usr/bin/env python
import unittest
import os
import noora
import argparse
import json
from noora.plugins.mssql.generate.GeneratePlugin import GeneratePlugin
from noora.system.App import App


class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDropPass(self):
        NOORA_DIR = os.path.dirname(noora.__file__)
        CURRENT_DIR = os.path.abspath('.')

        properties = dict()
        properties["noora.dir"] = NOORA_DIR
        properties["current.dir"] = CURRENT_DIR
        properties["plugin.dir"] = os.path.join(NOORA_DIR, 'plugins')
        properties["project.file"] = "myproject.json"

        app = App()
        f = app.get_config_file(properties)
        f = open(f.get_url())

        data = json.load(f)
        for key in data.keys():
            properties[key] = data[key]

        parser = argparse.ArgumentParser(description="mynoora, a sql deployment tool", add_help=False)
        parser.add_argument("commands", help="display a square of a given number", type=str, nargs='+')
        parser.add_argument('-r', action='store_true', help='show the revision')
        parser.add_argument('-v', type=str, help='version', required=False)

        arguments = parser.parse_args(['generate'])

        plugin = GeneratePlugin()
        plugin.execute(arguments, properties)


if __name__ == '__main__':
    unittest.main()
