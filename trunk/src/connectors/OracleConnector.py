#!/usr/bin/env python

import core.Connector as Connector
import os
import subprocess
import core.NooraException as NooraException

class OracleConnector(Connector.Connector):
  
  def __init__(self):
    Connector.Connector.__init__(self)
  
  def getScriptDir(self):
    return self.getNooraDir()+os.sep+'scripts'
  
  def execute(self, oracleSid, oracleUser, oraclePasswd, oracleScript, paramA, paramB):
    projectHelper=self.getProjectHelper()
    handle=open('feedback.log','wb')
    connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
    templateScript=projectHelper.cleanPath('@'+self.getScriptDir()+os.sep+'template.sql')
    result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript, paramA, paramB],shell=False,stdout=handle,stderr=handle)    
    if result!=0:
      stream=projectHelper.readFile('feedback.log')
      raise NooraException.NooraException(stream)
      




