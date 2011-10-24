#!/usr/bin/env python

import core.Plugin as Plugin
import core.VersionHelper as VersionHelper
import core.NooraException as NooraException
import os
import subprocess


class UpdatePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("UPDATE")
    
    self.addParameterDefinition('database',['-s','-si','--sid'])
    self.addParameterDefinition('scheme',['-u','-sc','--scheme'])
    self.addParameterDefinition('environment',['-e','--env'])
    self.addParameterDefinition('version',['-v','--version'])

  def getDescription(self):
    return "executes the defined update scripts in the alter folders."

  def getUsage(self):  
    print "Noora database installer, update.py"
    print self.getDescription()
    print "-s= --sid=     required, contains the tnsname of the database."
    print "-v= --version= required, contains the version of the update"
    print "                         to execute"
    print "-u= --scheme=  not required, contains the scheme of "
    print "                             the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "                             the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "                             packages, triggers and views."

  def getPluginDir(self):
    return self.getNooraDir()+os.sep+'plugins'+os.sep+'static'+os.sep+'update'

  def getPreviousVersion(self, versions, version):

    index=versions.index(version)
    if index>0:
      previousVersion=versions[index-1]
      return previousVersion    
    return None
  
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


  def installComponent(self, url, oracleSid, oracleUser, oraclePasswd):
    projectHelper=self.getProjectHelper()
    handle=open('feedback.log','wb')
    result=subprocess.call(['python',url+os.sep+'setup.py','-s='+oracleSid,'-u='+oracleUser,'-p='+oraclePasswd,'-silent'],shell=False,stdout=handle,stderr=handle)
    if result!=0:
      stream=projectHelper.readFile('feedback.log')
      raise NooraException.NooraException(stream)


  def installFiles(self, folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    projectHelper=self.getProjectHelper()
    files=projectHelper.findFiles(folder)
    for file in files:
      url=folder+os.sep+file
      print url.split(self.getBaseDir())[1]
      if projectHelper.getFileExtension(file).lower()=='zip':
        projectHelper.extractFile(url)
        extractFolder=projectHelper.getFileRoot(url)
        self.installComponent(extractFolder,oracleSid,oracleUser,oraclePasswd)
        projectHelper.removeFolderRecursive(extractFolder)
      else:
        connector.execute(oracleSid, oracleUser, oraclePasswd, url,'','', ignoreErrors)        


  def checkVersion(self, oracleSid,oracleUser,oraclePasswd,previousVersion, versionSelectStatement, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getPluginDir()+os.sep+'checkversion.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,previousVersion,versionSelectStatement,ignoreErrors)

  def checkEnvironment(self, oracleSid,oracleUser,oraclePasswd, environment, environmentSelectStatement, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getPluginDir()+os.sep+'checkenvironment.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,environment,environmentSelectStatement, ignoreErrors)

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
    projectHelper.failOnNone(schemes,'the variable SCHEMES is not set.')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    projectHelper.failOnNone(environment,'the variable DEFAULT_ENVIRONMENT is not set.')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    objects = configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnNone(objects,'the variable CREATE_OBJECTS is not set.')
    projectHelper.failOnEmpty(environment,'the variable CREATE_OBJECTS is not set.')

    defaultVersion=self.getDefaultVersion()
    projectHelper.failOnNone(defaultVersion,'the variable DEFAULT_VERSION is not set.')
    projectHelper.failOnEmpty(defaultVersion,'the variable DEFAULT_VERSION is not configured for this project.')

    version=parameterHelper.getParameterValue(['-v=','--version='],[])
    projectHelper.failOnEmpty(version,'no version was given')
    
    # find the versions
    versions=self.getVersions(defaultVersion)    
    version=version[0]
    projectHelper.failOnValueNotFound(versions,version,'the given version is not valid for this project.')
    
    projectHelper.failOnFolderNotPresent(self.getAlterDir()+os.sep+version,'the update folder for this version is not present.')

    previousVersion=self.getPreviousVersion(versions,version)
    projectHelper.failOnNone(previousVersion,'the previous version of this version could not be found.')

    versionScheme=configReader.getValue('VERSION_SCHEME')
    projectHelper.failOnNone(previousVersion,'the variable VERSION_SCHEME is not set.')
    oracleUser=projectHelper.getOracleUser(oracleSid, versionScheme)
    oraclePasswd=projectHelper.getOraclePasswd(oracleSid, versionScheme)

    versionSelectStatement=configReader.getValue('VERSION_SELECT_STATEMENT')
    projectHelper.failOnNone(versionSelectStatement,'the variable VERSION_SELECT_STATEMENT is not set.')
    environmentSelectStatement=configReader.getValue('ENVIRONMENT_SELECT_STATEMENT')
    projectHelper.failOnNone(versionSelectStatement,'the variable ENVIRONMENT_SELECT_STATEMENT is not set.')
    self.checkVersion(oracleSid,oracleUser,oraclePasswd,previousVersion,versionSelectStatement, ignoreErrors)
    self.checkEnvironment(oracleSid,oracleUser,oraclePasswd,environment,environmentSelectStatement, ignoreErrors)

    for scheme in schemes:

      print "updating scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)

      for object in objects:

        # global ddl objects
        folder=self.getAlterDir()+os.sep+version+os.sep+scheme+os.sep+'ddl'+os.sep+object
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)
      
        # environment specific ddl objects
        folder=self.getAlterDir()+os.sep+version+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

      # global dat objects
      folder=self.getAlterDir()+os.sep+version+os.sep+scheme+os.sep+'dat'
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

      # environment specific dat objects
      folder=self.getAlterDir()+os.sep+version+os.sep+scheme+os.sep+'dat'+os.sep+environment
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)
   
      print "scheme '"+scheme+"' updated."

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd, ignoreErrors)
        print "scheme '"+scheme+"' compiled."


