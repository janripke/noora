#!/usr/bin/env python
import noora
import argparse
import os
import json
from noora.system.Properties import Properties
from noora.system.App import App
from noora.system.ClassLoader import ClassLoader
from noora.plugins.Fail import Fail

NOORA_DIR = os.path.dirname(__file__)
CURRENT_DIR = os.path.abspath('.')


def main(args=None):
    properties = Properties()
    properties.set_property("noora.dir", NOORA_DIR)
    properties.set_property("current.dir", CURRENT_DIR)
    properties.set_property("plugin.dir", os.path.join(NOORA_DIR, 'plugins'))
    properties.set_property("project.file", "myproject.json")

    # find the project config file myproject.json, in the current folder or in the noora folder
    app = App()
    f = app.get_config_file(properties)
    f = open(f.get_url())

    data = json.load(f)
    for key in data.keys():
        properties.set_property(key, data[key])

    # Instantiate the argument parser
    parser = argparse.ArgumentParser(description="mynoora, a mysql deployment tool", add_help=False)
    parser.add_argument("commands", help="display a square of a given number", type=str, nargs='+', required=False)
    parser.add_argument('-r', action='store_true', help='show the revision')
    parser.add_argument('-v', type=str, help='version', required=False)
    parser.add_argument('-h', type=str, help='host', required=False)
    parser.add_argument('-d', type=str, help='database', required=False)
    parser.add_argument('-e', type=str, help='environment', required=False)
    parser.add_argument('-a', type=str, help='alias', required=False)

    args = parser.parse_args(args)

    # show the revision
    if args.r:
        print noora.__title__ + " version " + noora.__version__
        exit(0)

    # execute the given commands
    commands = args.commands
    Fail.fail_on_no_command(commands)

    for command in commands:
        plugin = App.find_plugin(command, properties)
        Fail.fail_on_invalid_plugin(plugin)
        plugin.execute(args, properties)


if __name__ == "__main__":
    main(args=None)


