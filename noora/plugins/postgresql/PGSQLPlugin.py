from noora.plugins.Plugin import Plugin

from noora.connectors.PGSQLConnector import PGSQLConnector


class PGSQLPlugin(Plugin):
    _connectable = PGSQLConnector
