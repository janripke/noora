#!/usr/bin/env python

import core.Plugin as Plugin
import os


class CreatePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("CREATE")

  def getUsage(self):  
    print "NoOra database installer, create.py"
    print "executes the defined baseline scripts in the create folder"
    print "-s= --sid=     required contains the tnsname of the database."
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "               the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "               packages, triggers and views."
    

  def getCreateDir(self):
    return self.getBaseDir()+os.sep+'create'

  def recompile(self, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getScriptDir()+os.sep+'recompile.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,'','', ignoreErrors)


  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    

    ignoreErrors=False  
    if  parameterHelper.hasParameter('-ignore_errors')==True:
      ignoreErrors=True      
      

    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()

    oracleSid=parameterHelper.getParameterValue(['-s=','--sid='],[])
    projectHelper.failOnEmpty(oracleSid,'no oracle sid was given.')
    configReader.failOnValueNotFound('ORACLE_SIDS',oracleSid,'the given oracle sid is not valid for this project.')
    oracleSid=oracleSid[0]
    
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    connector=self.getConnector()

    for scheme in schemes:
      print "creating scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)

      url=self.getCreateDir()+os.sep+scheme+os.sep+'install_scheme_'+environment+'.sql'
      projectHelper.failOnFileNotPresent(url,scheme+os.sep+'install_scheme_'+environment+'.sql not found, try to build this scheme.')
      connector.execute(oracleSid, oracleUser, oraclePasswd, url,'','', ignoreErrors)
    
      print "scheme '"+scheme+"' created."

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd, ignoreErrors)
        print "scheme '"+scheme+"' compiled."


