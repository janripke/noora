from noora.connectors.ConnectorException import ConnectorException


class Connectable:
    def __init__(self):
        pass

    def execute(self, executable, properties):
        raise ConnectorException("method not implemented")
