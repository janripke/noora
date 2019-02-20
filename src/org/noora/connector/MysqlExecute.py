#!/usr/bin/env python
from org.noora.connector.Execute import Execute

__revision__ = "$Revision: $"


class MysqlExecute(Execute):

  def __init__(self):
    Execute.__init__(self)
    self.__host = None
    self.__database = None
    self.__username = None
    self.__password = None
        
  def setHost(self, host):
    self.__host=host

  def getHost(self):
    return self.__host

  def setDatabase(self, database):
    self.__database=database

  def getDatabase(self):
    return self.__database
  
  def setUsername(self, username):
    self.__username=username

  def getUsername(self):
    return self.__username
  
  def setPassword(self, password):
    self.__password=password

  def getPassword(self):
    return self.__password    

    
    

