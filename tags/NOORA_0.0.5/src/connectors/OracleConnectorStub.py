#!/usr/bin/env python

import core.Connector as Connector
import os
import subprocess


class OracleConnectorStub(Connector.Connector):
  
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
    pass




