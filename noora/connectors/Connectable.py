from noora.exceptions.ConnectorException import ConnectorException


class Connectable(object):
    """
    Abstract connector class indicating if an object is 'connectable', i.e.,
    can connect to a database and execute queries.
    """
    def execute(self, executable, properties):
        raise ConnectorException("method not implemented")
