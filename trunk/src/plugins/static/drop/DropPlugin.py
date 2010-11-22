#!/usr/bin/env python

import core.Plugin as Plugin
import os
import sys
import subprocess

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
DROP_DIR     = NOORA_DIR+os.sep+'plugins'+os.sep+'static'+os.sep+'drop'
SCRIPT_DIR   = NOORA_DIR+os.sep+'scripts'

class DropPlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("DROP")


  def getUsage(self):
    print "NoOra database installer, drop.py"
    print "drops the database objects of the defined schemes."
    print "-s=  --sid=     required contains the tnsname of the database."
    print "-u=  --scheme=  not required, contains the scheme of "
    print "                the database objects to drop."
    print "-e=  --env=     not required, used for mapping "
    print "                the username and password."


  def showErrors(self):
    try:
      projectHelper=self.getProjectHelper()
      stream=projectHelper.readFile('feedback.log')
      print stream
    except:
      exit(1)

  def executeSqlplus(self, oracleSid, oracleUser, oraclePasswd, oracleScript):
    projectHelper=self.getProjectHelper()
    connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
    templateScript=projectHelper.cleanPath('@'+SCRIPT_DIR+os.sep+'template.sql')
    result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript])
    if result!=0:
      self.showErrors()
      exit(1)

  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    

    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()

    oracleSid=parameterHelper.getParameterValue(['-s=','--sid='],[])
    projectHelper.failOnEmpty(oracleSid,'no oracle sid was given.')
    configReader.failOnValueNotFound('ORACLE_SIDS',oracleSid,'the given oracle sid is not valid for this project.')
    configReader.failOnValueFound('BLOCKED_ORACLE_SIDS',oracleSid,'dropping is blocked for the given oracle_sid.')
    oracleSid=oracleSid[0]
    
    schemes=configReader.getValue('SCHEMES')
    projectHelper.failOnNone(schemes,'the variable SCHEMES is not set.')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    projectHelper.failOnNone(environment,'the variable DEFAULT_ENVIRONMENT is not set.')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    oracleUsers=configReader.getValue('ORACLE_USERS')
    projectHelper.failOnNone(oracleUsers,'the variable ORACLE_USERS is not set.')
    objects = configReader.getValue('DROP_OBJECTS')
    projectHelper.failOnNone(objects,'the variable DROP_OBJECTS is not set.')

    for scheme in schemes:
      print "dropping scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
      for object in objects:
      
        # ddl objects
        folder=DROP_DIR+os.sep+object
        files=projectHelper.findFiles(folder)
        for file in files:
          url=folder+os.sep+file
          print scheme+':'+url.split(NOORA_DIR)[1]
          self.executeSqlplus(oracleSid, oracleUser, oraclePasswd, url)

      print "scheme '"+scheme+"' dropped."


