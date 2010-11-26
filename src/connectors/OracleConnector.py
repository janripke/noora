#!/usr/bin/env python

import core.Connector as Connector
import os
import subprocess


class OracleConnector(Connector.Connector):
  
  def __init__(self):
    Connector.Connector.__init__(self)
  
  def getScriptDir(self):
    return self.getNooraDir()+os.sep+'scripts'
  
  def showErrors(self):
    try:
      projectHelper=self.getProjectHelper()
      stream=projectHelper.readFile('feedback.log')
      print stream
    except:
      exit(1)

  def execute(self, oracleSid, oracleUser, oraclePasswd, oracleScript, paramA, paramB):
    projectHelper=self.getProjectHelper()
    connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
    templateScript=projectHelper.cleanPath('@'+self.getScriptDir()+os.sep+'template.sql')
    result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript, paramA, paramB])
    if result!=0:
      self.showErrors()
      exit(1)




