#!/usr/bin/env python

import core.Plugin as Plugin
import os


class UpdatePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("UPDATE")


  def getUsage(self):  
    print "Noora database installer, update.py"
    print "executes the defined update scripts in the alter folders."
    print "-s= --sid=     required, contains the tnsname of the database."
    print "-v= --version= required, contains the version of the update"
    print "                         to execute"
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "               the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "               packages, triggers and views."

  def getPluginDir(self):
    return self.getNooraDir()+os.sep+'plugins'+os.sep+'static'+os.sep+'update'

  def getPreviousVersion(self, version):
    configReader=self.getConfigReader()
    versions=configReader.getValue('VERSIONS')

    index=versions.index(version)
    if index>0:
      previousVersion=versions[index-1]
      return previousVersion    
    return None


  def checkVersion(self, oracleSid,oracleUser,oraclePasswd,previousVersion, versionSelectStatement,ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getPluginDir()+os.sep+'checkversion.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,previousVersion,versionSelectStatement,ignoreErrors)


  def checkEnvironment(self, oracleSid,oracleUser,oraclePasswd, environment, environmentSelectStatement,ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getPluginDir()+os.sep+'checkenvironment.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,environment,environmentSelectStatement,ignoreErrors)
 

  def recompile(self, oracleSid, oracleUser, oraclePasswd,ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getPluginDir()+os.sep+'recompile.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,'', '',ignoreErrors)


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


    version=parameterHelper.getParameterValue(['-v=','--version='],[])
    projectHelper.failOnEmpty(version,'no version was given')
    configReader.failOnValueNotFound('VERSIONS',version,'the given version is not valid for this project.')
    version=version[0]
    projectHelper.failOnFolderNotPresent(self.getAlterDir()+os.sep+version,'the update folder for this version is not present.')

    previousVersion=self.getPreviousVersion(version)
    projectHelper.failOnNone(previousVersion,'the previous version of this version could not be found.')

    versionScheme=configReader.getValue('VERSION_SCHEME')
    projectHelper.failOnNone(previousVersion,'the variable VERSION_SCHEME is not set.')
    oracleUser=projectHelper.getOracleUser(oracleSid, versionScheme)
    oraclePasswd=projectHelper.getOraclePasswd(oracleSid, versionScheme)

    versionSelectStatement=configReader.getValue('VERSION_SELECT_STATEMENT')
    projectHelper.failOnNone(versionSelectStatement,'the variable VERSION_SELECT_STATEMENT is not set.')
    environmentSelectStatement=configReader.getValue('ENVIRONMENT_SELECT_STATEMENT')
    projectHelper.failOnNone(versionSelectStatement,'the variable ENVIRONMENT_SELECT_STATEMENT is not set.')
    self.checkVersion(oracleSid,oracleUser,oraclePasswd,previousVersion,versionSelectStatement,ignoreErrors)
    self.checkEnvironment(oracleSid,oracleUser,oraclePasswd,environment,environmentSelectStatement,ignoreErrors)

    connector=self.getConnector()

    for scheme in schemes:

      print "updating scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)

      url=self.getAlterDir()+os.sep+version+os.sep+scheme+os.sep+'install_scheme_'+environment+'.sql'
      projectHelper.failOnFileNotPresent(url,scheme+os.sep+'install_scheme_'+environment+'.sql not found, try to build this scheme.')
      connector.execute(oracleSid, oracleUser, oraclePasswd, url,'','',ignoreErrors)
   
      print "scheme '"+scheme+"' updated."

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd, ignoreErrors)
        print "scheme '"+scheme+"' compiled."


