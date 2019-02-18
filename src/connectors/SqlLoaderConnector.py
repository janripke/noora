import logging
import os
import subprocess

import core.Connector as Connector
import core.NooraException as NooraException


class SqlLoaderConnector(Connector.Connector):
  def getScriptDir(self):
    return self.getNooraDir()+os.sep+'scripts'

  def getStartupInfo(self):
    startupInfo=None
    if os.name=='nt':    
      startupInfo=subprocess.STARTUPINFO()
      #USESHOWWINDOW
      startupInfo.dwFlags |=1
      #SW_HIDE
      startupInfo.wShowWindow=0
    return startupInfo

  def getDatabases(self):
    projectHelper=self.getProjectHelper()
    url=os.getenv('TNS_ADMIN')+os.sep+"tnsnames.ora"
    stream=projectHelper.readFile(url)
    print(stream)

  def execute(self, oracleSid, oracleUser, oraclePasswd, ctlFile, dataFile, ignoreErrors):
    try:
      startupInfo=self.getStartupInfo()
      projectHelper=self.getProjectHelper()
      handle=open('feedback.log','wb')
      connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
      controlString='control='+ctlFile
      dataString='data='+dataFile
      result=subprocess.call(['sqlldr',connectString , controlString, dataString],shell=False,stdout=handle,stderr=handle,startupinfo=startupInfo)
      stream=projectHelper.readFile('feedback.log')
     
      logger = logging.getLogger('NoOraLogger')
      logger.info(dataFile)
      if result!=0:  
        #stream = StreamHelper.StreamHelper().convert(stream)
        #stream = stream.replace(chr(10),chr(32))     
        logger.error(stream)
        if ignoreErrors==False:
          raise NooraException.NooraException(stream)
      else:
        logger.info(stream)
    except OSError:
      raise NooraException.NooraException("Could not execute sqlldr. Is it installed and in your path?")
