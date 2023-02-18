from abc import ABC

from noora.plugins.plugin import Plugin

from noora.connectors.mssql_connector import MssqlConnector


class MssqlPlugin(Plugin, ABC):
    _connectable = MssqlConnector
