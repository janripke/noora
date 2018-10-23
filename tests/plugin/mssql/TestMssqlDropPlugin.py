#!/usr/bin/env python
import unittest
import os
import noora
import argparse
import json
from noora.plugins.mssql.drop.DropPlugin import DropPlugin
from noora.system.App import App


class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDropPass(self):
        noora_dir = os.path.dirname(noora.__file__)
        current_dir = os.path.abspath('.')

        properties = dict()
        properties["noora.dir"] = noora_dir
        properties["current.dir"] = current_dir
        properties["plugin.dir"] = os.path.join(noora_dir, 'plugins')
        properties["project.file"] = "myproject.json"

        app = App()
        f = app.get_config_file(properties)
        f = open(f.get_url())

        data = json.load(f)
        for key in data.keys():
            properties[key] = data[key]

        parser = argparse.ArgumentParser(description="mynoora, a sql deployment tool", add_help=False)
        parser.add_argument("commands", help="display a square of a given number", type=str, nargs='+')
        parser.add_argument('-r', action='store_true', help='show the revision', required=False)
        parser.add_argument('-h', type=str, help='host', required=False)
        parser.add_argument('-s', type=str, help='schema', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        parser.add_argument('-a', type=str, help='alias', required=False)

        arguments = parser.parse_args(['drop', '-h=elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433'])

        plugin = DropPlugin()
        plugin.execute(arguments, properties)


if __name__ == '__main__':
    unittest.main()
