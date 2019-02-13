import noora

from noora.plugins.Plugin import Plugin


class HelpPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "help", None)

    def parse_args(self, parser, args):
        return parser.parse_args(args)

    def execute(self, arguments, properties):
        print(noora.__description__)
        print(noora.__uri__)
        print(noora.__version__)
