from noora.plugins.Plugin import Plugin

from noora.connectors.MssqlConnector import MssqlConnector


class MssqlPlugin(Plugin):
    __connectable = MssqlConnector
