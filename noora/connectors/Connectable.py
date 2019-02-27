from noora.exceptions.ConnectorException import ConnectorException


class Connectable(object):
    def execute(self, executable, properties):
        raise ConnectorException("method not implemented")
