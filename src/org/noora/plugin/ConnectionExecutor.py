#!/usr/bin/env python

import os
from org.noora.io.Files import Files
from org.noora.connector.ExecuteFactory import ExecuteFactory

class ConnectionExecutor:
  def __init__(self):
    pass
  
  @staticmethod
  def execute(connector, properties, folder, host, database, ignoreErrors, user, passwd):
    if folder.isDirectory():
      files = Files.list(folder)     
      for file in files:
        url = file.getPath()+os.sep+file.getName()        
        print url
        
        
        executor = ExecuteFactory.newMysqlExecute()
        executor.setHost(host)
        executor.setDatabase(database)
        executor.setIgnoreErrors(ignoreErrors)
        executor.setUsername(user)
        executor.setPassword(passwd)
        executor.setScript(file)
        
        connector.execute(executor, properties)
