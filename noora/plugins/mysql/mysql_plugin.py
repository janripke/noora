from abc import ABC

from noora.plugins.plugin import Plugin

from noora.connectors.mysql_connector import MysqlConnector


class MysqlPlugin(Plugin, ABC):
    _connectable = MysqlConnector
