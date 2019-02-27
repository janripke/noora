import argparse

from noora.plugins.Plugin import Plugin


class GeneratePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "generate", None)

    def parse_args(self, parser, args):
        parser.add_argument('-t', type=str, help='technology', required=True)
        return parser.parse_args(args)

    def execute(self, arguments, properties):
        # TODO: fail on no technology
        # TODO: fail on invalid technology

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

