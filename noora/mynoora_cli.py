#!/usr/bin/env python
import argparse
import os
import json
from noora.system.App import App
from noora.plugins.Fail import Fail
from os.path import expanduser
import noora


def main(args=None):
    properties = dict()
    properties["noora.dir"] = os.path.dirname(noora.__file__)
    properties["current.dir"] = os.path.abspath('.')
    properties["plugin.dir"] = os.path.join(properties.get('noora.dir'), 'plugins')
    properties["project.file"] = "myproject.json"
    properties['home.dir'] = expanduser('~')

    # find the project config file myproject.json, in the current folder or in the noora folder
    app = App()
    f = app.get_config_file(properties)
    f = open(f.get_url())

    data = json.load(f)
    for key in data.keys():
        properties[key] = data[key]

    # Instantiate the argument parser.
    parser = argparse.ArgumentParser(description="mynoora, a sql deployment tool", add_help=False)
    parser.add_argument("commands", help="command to execute", type=str, nargs='+')
    parser.add_argument('-r', action='store_true', help='show the revision', required=False)
    arguments, unknown = parser.parse_known_args(args)

    # show the revision
    if arguments.r:
        print(noora.__title__ + " version " + noora.__version__)
        exit(0)

    # execute the given commands
    commands = arguments.commands
    Fail.fail_on_no_command(commands)

    for command in commands:
        plugin = App.find_plugin(command, properties)
        Fail.fail_on_invalid_plugin(plugin)
        arguments = plugin.parse_args(parser, args)
        plugin.execute(arguments, properties)


if __name__ == "__main__":
    main(args=None)


