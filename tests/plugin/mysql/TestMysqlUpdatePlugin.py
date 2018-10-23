#!/usr/bin/env python
import unittest
import os
import noora
import argparse
import json
from noora.plugins.mysql.update.UpdatePlugin import UpdatePlugin
from noora.system.App import App


class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUpdatePass(self):
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

        parser = argparse.ArgumentParser(description="mynoora, a mysql deployment tool", add_help=False)
        parser.add_argument("commands", help="display a square of a given number", type=str, nargs='+')
        parser.add_argument('-r', action='store_true', help='show the revision')
        parser.add_argument('-v', type=str, help='version', required=False)
        parser.add_argument('-h', type=str, help='host', required=False)
        parser.add_argument('-d', type=str, help='database', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        parser.add_argument('-a', type=str, help='alias', required=False)

        arguments = parser.parse_args(['update', '-h=localhost', '-v=1.0.1'])

        plugin = UpdatePlugin()
        plugin.execute(arguments, properties)


if __name__ == '__main__':
    unittest.main()
