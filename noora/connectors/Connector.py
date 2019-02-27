from noora.connectors.Connectable import Connectable
from noora.exceptions.ConnectorException import ConnectorException


class Connector(Connectable):
    def execute(self, executable, properties):
        raise ConnectorException("method not implemented")
