#!/usr/bin/env python
from org.noora.connector.MysqlExecute import MysqlExecute
from org.noora.connector.OracleExecute import OracleExecute

class ExecuteFactory:
  def __init__(self):
    pass
  
  @staticmethod
  def newMysqlExecute():
    return MysqlExecute()
  
  @staticmethod
  def newOracleExecute():
    return OracleExecute()
