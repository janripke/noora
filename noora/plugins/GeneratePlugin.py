#!/usr/bin/env python
from noora.plugins.Plugin import Plugin
import argparse


class GeneratePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "generate", None)

    def execute(self, arguments, properties):
        # todo: fail on no technology
        # todo:fail on invalid technology

        # resolve the generate plugin to execute based on the given technology
        technology = arguments.t

        plugin = None
        if technology == 'mysql':
            from noora.plugins.mysql.generate.GeneratePlugin import GeneratePlugin
            plugin = GeneratePlugin()
        if technology == 'mssql':
            from noora.plugins.mssql.generate.GeneratePlugin import GeneratePlugin
            plugin = GeneratePlugin()

        # no arguments are allowed here, the project generator is assumed.
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-r', action='store_true', help='show the revision')
        parser.add_argument('-v', type=str, help='version', required=False)
        target_arguments = parser.parse_args([])

        plugin.execute(target_arguments, properties)

