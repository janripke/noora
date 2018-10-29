from noora.connectors.Connector import Connector


class MysqlConnectorStub(Connector):
    def __init__(self):
        Connector.__init__(self)
        self.__result = None

    def get_result(self):
        return self.__result

    def set_result(self, result):
        self.__result = result

    def execute(self, executable, properties):
        pass
