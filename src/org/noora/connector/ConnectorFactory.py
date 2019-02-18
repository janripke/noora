class ConnectorFactory(object):
  @staticmethod
  def newMysqlConnector():
    from org.noora.connector.MysqlConnector import MysqlConnector
    return MysqlConnector() 
  
  @staticmethod
  def newOracleConnector():
    from org.noora.connector.OracleConnector import OracleConnector
    return OracleConnector() 

  @staticmethod
  def newPostgresqlConnector():
    from org.noora.connector.PostgresqlConnector import PostgresqlConnector
    return PostgresqlConnector()

  @staticmethod
  def newTripolisDeployEmailConnector():
    from org.noora.connector.TripolisDeployEmailConnector import TripolisDeployEmailConnector
    return TripolisDeployEmailConnector()
