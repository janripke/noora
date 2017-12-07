from noora.plugins.Plugin import Plugin
import noora


class HelpPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "help", None)

    def execute(self, arguments, properties):
        print noora.__description__
        print noora.__uri__
        print noora.__version__
