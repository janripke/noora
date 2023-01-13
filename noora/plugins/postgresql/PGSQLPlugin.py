from abc import ABC

from noora.plugins.Plugin import Plugin


from noora.connectors.PGSQLConnector import PGSQLConnector


class PGSQLPlugin(Plugin, ABC):
    _connectable = PGSQLConnector
