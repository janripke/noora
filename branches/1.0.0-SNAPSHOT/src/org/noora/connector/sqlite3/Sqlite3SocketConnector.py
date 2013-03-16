from org.noora.connector.Connector import Connector


class Sqlite3SocketConnector(object):

  def __init__(self, connectorContext):
    Connector.__init__(self, connectorContext)
  
  def execute(self, executable, properties):
    pass