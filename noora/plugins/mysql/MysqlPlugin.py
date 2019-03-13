from noora.plugins.Plugin import Plugin

from noora.connectors.MysqlConnector import MysqlConnector


class MysqlPlugin(Plugin):
    _connectable = MysqlConnector
