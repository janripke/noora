#!/usr/bin/env python

import core.Plugin          as Plugin
import core.VersionHelper   as VersionHelper
import core.NooraException  as NooraException
import core.ClassLoader     as ClassLoader
import core.ParameterHelper as ParameterHelper
import os
import sys
import subprocess
import traceback

class RecreatePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("RECREATE")
    
    self.addParameterDefinition('database',['-s','-si','--sid'])
    self.addParameterDefinition('scheme',['-u','-sc','--scheme'])
    self.addParameterDefinition('environment',['-e','--env'])
    self.addParameterDefinition('version',['-m','--max'])
    
  def getDescription(self):
    return "recreates the database objects of the defined schemes."


  def getUsage(self):  
    print "NoOra database installer, recreate.py"
    print self.getDescription()
    print "-s= --sid=     required contains the tnsname of the database."
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "               the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "               packages, triggers and views."  
    print "-m= --max=     not required, after the given version recreation will stop."
    print "-test          not required, executes the defined unit tests after recreation."


  def getMaxVersion(self,versions):
    return versions[len(versions)-1]
  
  def getDefaultVersion(self):
    configReader=self.getConfigReader()
    defaultVersion=configReader.getValue('DEFAULT_VERSION')
    return defaultVersion
  
  def getVersions(self, defaultVersion):
    projectHelper=self.getProjectHelper()    
    versions=[]
    alterFolder=projectHelper.getAlterFolder()
    if projectHelper.folderPresent(alterFolder):
      versions=projectHelper.findFolders(alterFolder)
    createFolder=projectHelper.getCreateFolder()
    if projectHelper.folderPresent(createFolder):
      versions.append(defaultVersion)
    versionHelper=VersionHelper.VersionHelper(versions)
    versions=versionHelper.sort()
    return versions  
  
  def getPlugin(self, plugins, pluginType):
    classLoader = ClassLoader.ClassLoader()
    for plugin in plugins:
      pluginClass=classLoader.findByPattern(plugin)
      if pluginClass.getType().lower()==pluginType.lower():
        return pluginClass


  def addParameter(self, parameters, parameterType, parameterValue):
    if parameterValue:
      parameters.append(parameterType+parameterValue)
    return parameters
  
  def addOption(self, parameters, optionType):
    parameters.append(optionType)
    return parameters

  def dropDatabase(self, plugins, oracleSid, scheme, environment):
    try:
      dropPlugin = self.getPlugin(plugins, 'drop')
      parameters=[]
      parameters=self.addParameter(parameters, "--sid=", oracleSid)
      parameters=self.addParameter(parameters, "--scheme=", scheme)
      parameters=self.addParameter(parameters, "--env=", environment)
    
      parameterHelper=ParameterHelper.ParameterHelper()
      parameterHelper.setParameters(parameters)
      dropPlugin.execute(parameterHelper)
    except NooraException.NooraException as e:
      print e.getMessage()    
      exit(1)
    except Exception as e:
      print traceback.print_exc()
      exit(1)


  def createDatabase(self, plugins, oracleSid, scheme, environment):
    try:
      createPlugin = self.getPlugin(plugins, 'create')
      parameters=[]
      
      parameters=self.addParameter(parameters, "--sid=", oracleSid)
      parameters=self.addParameter(parameters, "--scheme=", scheme)
      parameters=self.addParameter(parameters, "--env=", environment)
      parameters=self.addOption(parameters, "-nocompile")
    
      parameterHelper=ParameterHelper.ParameterHelper()
      parameterHelper.setParameters(parameters)
      createPlugin.execute(parameterHelper)
    except NooraException.NooraException as e:
      print e.getMessage()    
      exit(1)
    except:
      print traceback.print_exc()
      exit(1)

  def updateDatabase(self, plugins, oracleSid, scheme, environment, versions, maxVersion):
    try:
      for version in versions:
        if version!=versions[0]:
        
          updatePlugin = self.getPlugin(plugins, 'update')
          parameters=[]
          parameters=self.addParameter(parameters, "--sid=", oracleSid)
          parameters=self.addParameter(parameters, "--scheme=", scheme)
          parameters=self.addParameter(parameters, "--env=", environment)
          parameters=self.addParameter(parameters, "--version=", version)
          parameters=self.addOption(parameters, "-nocompile")
    
          parameterHelper=ParameterHelper.ParameterHelper()
          parameterHelper.setParameters(parameters)
          updatePlugin.execute(parameterHelper)
          
        if version==maxVersion:
          break
          
    except NooraException.NooraException as e:
      print e.getMessage()    
      exit(1)
    except:
      print traceback.print_exc()
      exit(1)
      

  def recompile(self, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getScriptDir()+os.sep+'recompile.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,'','', ignoreErrors)

  def unittest(self, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getScriptDir()+os.sep+'unittest.sql'
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

    scheme=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],[""])
    scheme=scheme[0]
    
    
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    defaultVersion=self.getDefaultVersion()
    projectHelper.failOnEmpty(defaultVersion,'the variable DEFAULT_VERSION is not configured for this project.')

    # find the versions
    versions=self.getVersions(defaultVersion)
    
    maxVersion=self.getMaxVersion(versions)
    maxVersion=parameterHelper.getParameterValue(['-m=','--max='],[maxVersion])
    maxVersion=maxVersion[0]
    projectHelper.failOnValueNotFound(versions,maxVersion,'the given max version is not valid for this project.')
    
    plugins=configReader.getValue('PLUGINS')
    projectHelper.failOnNone(plugins,'the variable PLUGINS is not set.')
    projectHelper.failOnEmpty(plugins,'the variable PLUGINS is not set.')
        

    self.dropDatabase(plugins, oracleSid, scheme, environment)
    self.createDatabase(plugins, oracleSid, scheme, environment)
    self.updateDatabase(plugins, oracleSid, scheme, environment, versions, maxVersion)

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd, ignoreErrors)
        print "scheme '"+scheme+"' compiled."

    if parameterHelper.hasParameter('-test')==True:
      for scheme in schemes:
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.unittest(oracleSid, oracleUser, oraclePasswd, ignoreErrors)


