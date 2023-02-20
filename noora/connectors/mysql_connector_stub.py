from noora.connectors.connector import Connector


class MysqlConnectorStub(Connector):
    def execute(self, executable, properties):
        pass
