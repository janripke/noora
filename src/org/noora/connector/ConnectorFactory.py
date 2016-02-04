from org.noora.connector.MysqlConnector import MysqlConnector
from org.noora.connector.OracleConnector import OracleConnector
from org.noora.connector.PostgresqlConnector import PostgresqlConnector
from org.noora.connector.TripolisDeployEmailConnector import TripolisDeployEmailConnector

class ConnectorFactory:
  def __init__(self):
    pass
  
  @staticmethod
  def newMysqlConnector():
    return MysqlConnector() 
  
  @staticmethod
  def newOracleConnector():
    return OracleConnector() 

  @staticmethod
  def newPostgresqlConnector():
    return PostgresqlConnector()

  @staticmethod
  def newTripolisDeployEmailConnector():
    return TripolisDeployEmailConnector()