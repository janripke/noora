from org.noora.connector.Connectable import Connectable
from org.noora.connector.ConnectorContext import ConnectorContext
from org.noora.connector.oracle.OracleCommandConnector import OracleCommandConnector
from org.noora.connector.oracle.OracleSocketConnector import OracleSocketConnector


class ConnectorFactory:
  # create a Connector or ConnectorContext on request.
  # Keep it simple for now and just hard-wire class selection.
  
  DATABASE_ORACLE = 'Oracle'
  DATABASE_MYSQL  = 'Mysql'
  DATABASE_SQLITE = 'Sqlite'
  DATABASE_STUB   = 'Stub'

  def __init__(self):
    pass

  def createConnector(self, database, connectionType):
    connectorContext = ConnectorFactory.createConnectorContext()
    
    if (database == ConnectorFactory.DATABASE_ORACLE):
      if (connectionType == Connectable.CONNECTOR_TYPE_CMD):
        return OracleCommandConnector(connectorContext)
      else:
        return OracleSocketConnector(connectorContext)
    return None
  
  @classmethod
  def createConnectorContext(cls):
    return ConnectorContext()