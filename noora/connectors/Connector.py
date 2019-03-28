from noora.connectors.Connectable import Connectable
from noora.exceptions.ConnectorException import ConnectorException


class Connector(Connectable):
    def __init__(self):
        self.__result = None

    def get_result(self):
        return self.__result

    def set_result(self, result):
        self.__result = result

    def execute(self, executable, properties):
        raise ConnectorException("method not implemented")
