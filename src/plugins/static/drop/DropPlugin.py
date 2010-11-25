#!/usr/bin/env python

import core.Plugin as Plugin
import os

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


  def getDropDir(self):
    return self.getNooraDir()+os.sep+'plugins'+os.sep+'static'+os.sep+'drop'
  
  def getScriptDir(self):
    return self.getNooraDir()+os.sep+'scripts'

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

    connector=self.getConnector()

    for scheme in schemes:
      print "dropping scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
      for object in objects:
      
        # ddl objects
        folder=self.getDropDir()+os.sep+object
        files=projectHelper.findFiles(folder)
        for file in files:
          url=folder+os.sep+file
          print scheme+':'+url.split(self.getNooraDir())[1]
          connector.execute(oracleSid, oracleUser, oraclePasswd, url)

      print "scheme '"+scheme+"' dropped."


