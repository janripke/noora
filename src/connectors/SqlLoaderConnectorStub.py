import os

import core.Connector as Connector


class SqlLoaderConnectorStub(Connector.Connector):
  def getScriptDir(self):
    return self.getNooraDir()+os.sep+'scripts'
  
  def showErrors(self):
    try:
      projectHelper=self.getProjectHelper()
      stream=projectHelper.readFile('feedback.log')
      print(stream)
    except:
      exit(1)

  def execute(self, oracleSid, oracleUser, oraclePasswd, ctlFile, dataFile, ignoreErrors):
    pass
