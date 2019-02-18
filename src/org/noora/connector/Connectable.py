from org.noora.connector.ConnectorException import ConnectorException

__revision__ = "$Revision: $"


class Connectable(object):
  def execute(self, executable):
    raise ConnectorException("method not implemented")

