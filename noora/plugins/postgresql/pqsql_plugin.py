from abc import ABC

from noora.plugins.plugin import Plugin


from noora.connectors.pgsql_connector import PGSQLConnector


class PGSQLPlugin(Plugin, ABC):
    _connectable = PGSQLConnector
