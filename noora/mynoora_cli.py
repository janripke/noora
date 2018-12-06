#!/usr/bin/env python
import os
from noora.system.App import App
from noora.plugins.Fail import Fail
from os.path import expanduser
import noora


def main(args=None):
    # retrieve the basic properties.
    properties = App.properties()

    # load the properties from myproject.json, in the current folder or in the noora folder
    App.load_properties(properties)

    # retrieve the basic mynoora parser.
    parser = App.get_parser()
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


