#!/usr/bin/env python
import unittest
import os
import noora
import argparse
import json
from noora.plugins.GeneratePlugin import GeneratePlugin
from noora.system.Properties import Properties
from noora.system.App import App
import noora


class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGeneratePass(self):
        properties = Properties()
        properties.set_property("noora.dir", noora.__file__)
        properties.set_property("current.dir", os.path.abspath('.'))
        properties.set_property("plugin.dir", os.path.join(properties.get('noora.dir'), 'plugins'))
        properties.set_property("project.file", "myproject.json")

        app = App()
        f = app.get_config_file(properties)
        f = open(f.get_url())

        data = json.load(f)
        for key in data.keys():
            properties.set_property(key, data[key])

        parser = argparse.ArgumentParser(description="mynoora, a sql deployment tool", add_help=False)
        parser.add_argument("commands", help="display a square of a given number", type=str, nargs='+')
        parser.add_argument('-r', action='store_true', help='show the revision')
        parser.add_argument('-t', type=str, help='version', required=False)

        arguments = parser.parse_args(['generate', '-t=mssql'])

        plugin = GeneratePlugin()
        plugin.execute(arguments, properties)


if __name__ == '__main__':
    unittest.main()
