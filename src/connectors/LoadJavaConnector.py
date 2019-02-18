import os
import logging
import subprocess
from subprocess import Popen, PIPE

import core.Connector as Connector
import core.NooraException as NooraException


class LoadJavaConnector(Connector.Connector):
  def getScriptDir(self):
    return self.getNooraDir() + os.sep + 'scripts'

  def getStartupInfo(self):
    startupInfo = None
    if os.name == 'nt':
      startupInfo = subprocess.STARTUPINFO()
      # USESHOWWINDOW
      startupInfo.dwFlags |= 1
      # SW_HIDE
      startupInfo.wShowWindow = 0
    return startupInfo

  def getDatabases(self):
    projectHelper = self.getProjectHelper()
    url = os.getenv('TNS_ADMIN') + os.sep + "tnsnames.ora"
    stream = projectHelper.readFile(url)
    print(stream)

  def execute(self, oracleSid, oracleUser, oraclePasswd, oracleScript, paramA, paramB, ignoreErrors):
    try:
      startupInfo = self.getStartupInfo()
      projectHelper = self.getProjectHelper()
      handle = open('feedback.log', 'wb')
      credentials = oracleUser + '/' + oraclePasswd + '@' + oracleSid

      statement = 'loadjava -user ' + credentials + ' -resolve -force ' + projectHelper.cleanPath(oracleScript)
      p = Popen([statement], stdout=PIPE, shell=True)
      output, error = p.communicate()

      # # templateScript='@'+projectHelper.cleanPath(self.getScriptDir()+os.sep+'template.sql')
      # print executeList
      # result = subprocess.call(executeList, shell=True, stdout=handle, stderr=handle, startupinfo=startupInfo)
      # stream = projectHelper.readFile('feedback.log')

      logger = logging.getLogger('NoOraLogger')
      logger.info(oracleScript)
      if error:
        # stream = StreamHelper.StreamHelper().convert(stream)
        # stream = stream.replace(chr(10),chr(32))
        logger.error(error)
        if ignoreErrors == False:
          raise NooraException.NooraException(error)
      else:
        logger.info(output)
    except OSError:
      raise NooraException.NooraException("Could not execute loadjava. Is it installed and in your path?")
