from org.noora.connector.MysqlExecute import MysqlExecute
from org.noora.connector.PostgresqlExecute import PostgresqlExecute
from org.noora.connector.OracleExecute import OracleExecute
from org.noora.connector.TripolisExecute import TripolisExecute


class ExecuteFactory(object):
  @staticmethod
  def newMysqlExecute():
    return MysqlExecute()
  
  @staticmethod
  def newPostgresqlExecute():
    return PostgresqlExecute()

  @staticmethod
  def newOracleExecute():
    return OracleExecute()

  @staticmethod
  def newTripolisExecute():
    return TripolisExecute()
