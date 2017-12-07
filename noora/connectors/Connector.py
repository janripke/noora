from noora.connectors.Connectable import Connectable
from noora.connectors.ConnectorException import ConnectorException


class Connector(Connectable):
    def __init__(self):
        Connectable.__init__(self)

    def execute(self, executable, properties):
        raise ConnectorException("method not implemented")
