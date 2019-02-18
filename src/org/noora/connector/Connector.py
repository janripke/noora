from org.noora.connector.Connectable import Connectable
from org.noora.connector.ConnectorException import ConnectorException

__revision__ = "$Revision: $"


class Connector(Connectable):
  def execute(self, executable, properties):
    raise ConnectorException("method not implemented")
