from noora.plugins.Plugin import Plugin

from noora.connectors.MssqlConnector import MssqlConnector


class MssqlPlugin(Plugin):
    _connectable = MssqlConnector
