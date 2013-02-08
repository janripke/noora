#!/usr/bin/env python

import core.Connector as Connector
import os
import subprocess
import core.NooraException as NooraException
import logging

class OracleConnector(Connector.Connector):
  
  def __init__(self):
    Connector.Connector.__init__(self)
  
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
    print stream
    
  
  def execute(self, oracleSid, oracleUser, oraclePasswd, oracleScript, paramA, paramB, ignoreErrors):
    try:
      startupInfo=self.getStartupInfo()
      projectHelper=self.getProjectHelper()
      handle=open('feedback.log','wb')
      connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
      templateScript=projectHelper.cleanPath('@'+self.getScriptDir()+os.sep+'template.sql')
      result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript, paramA, paramB],shell=False,stdout=handle,stderr=handle,startupinfo=startupInfo)
      stream=projectHelper.readFile('feedback.log')
     
      
      logger = logging.getLogger('NoOraLogger')
      logger.info(oracleScript)
      if result!=0:  
        #stream = StreamHelper.StreamHelper().convert(stream)
        #stream = stream.replace(chr(10),chr(32))     
        logger.error(stream)
        if ignoreErrors==False:
          raise NooraException.NooraException(stream)
      else:
        logger.info(stream)
    except OSError:
      raise NooraException.NooraException("Could not execute sqlplus. Is it installed and in your path?")




