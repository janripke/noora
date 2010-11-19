#!/usr/bin/env python

import core.Plugin as Plugin
import core.VersionHelper as VersionHelper
import os
import sys
import subprocess

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR     = os.path.abspath('.')
ALTER_DIR    = BASE_DIR+os.sep+'alter'
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'+os.sep+'static'+os.sep+'update'
SCRIPT_DIR   = NOORA_DIR+os.sep+'scripts'


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
    print "                             the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "                             the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "                             packages, triggers and views."

  def showErrors(self):
    try:
      projectHelper=self.getProjectHelper()
      stream=projectHelper.readFile('feedback.log')
      print stream
    except:
      exit(1)

  def getPreviousVersion(self, versions, version):

    index=versions.index(version)
    if index>0:
      previousVersion=versions[index-1]
      return previousVersion    
    return None


  def executeSqlplus(self, oracleSid, oracleUser, oraclePasswd, oracleScript, paramA, paramB):
    projectHelper=self.getProjectHelper()      
    connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
    templateScript=projectHelper.cleanPath('@'+SCRIPT_DIR+os.sep+'template.sql')
    result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript, paramA, paramB])
    if result!=0:
      self.showErrors()
      exit(1)

  def installComponent(self, url, oracleSid, oracleUser, oraclePasswd):
    result=subprocess.call(['python',url+os.sep+'setup.py','-s='+oracleSid,'-u='+oracleUser,'-p='+oraclePasswd])
    if result!=0:
      exit(1)

  def installFiles(self, folder, oracleSid, oracleUser, oraclePasswd):
    projectHelper=self.getProjectHelper()
    files=projectHelper.findFiles(folder)
    for file in files:
      url=folder+os.sep+file
      print url.split(BASE_DIR)[1]
      if projectHelper.getFileExtension(file).lower()=='zip':
        projectHelper.extractFile(url)
        extractFolder=projectHelper.getFileRoot(url)
        self.installComponent(extractFolder,oracleSid,oracleUser,oraclePasswd)
        projectHelper.removeFolderRecursive(extractFolder)
      else:
        self.executeSqlplus(oracleSid, oracleUser, oraclePasswd, url,'','')  


  def checkVersion(self, oracleSid,oracleUser,oraclePasswd,previousVersion, versionSelectStatement):
    oracleScript=PLUGIN_DIR+os.sep+'checkversion.sql'
    self.executeSqlplus(oracleSid,oracleUser,oraclePasswd, oracleScript,previousVersion,versionSelectStatement)

  def checkEnvironment(self, oracleSid,oracleUser,oraclePasswd, environment, environmentSelectStatement):
    oracleScript=PLUGIN_DIR+os.sep+'checkenvironment.sql'
    self.executeSqlplus(oracleSid,oracleUser,oraclePasswd, oracleScript,environment,environmentSelectStatement)
 

  def recompile(self, oracleSid, oracleUser, oraclePasswd):
    oracleScript=SCRIPT_DIR+os.sep+'recompile.sql'
    self.executeSqlplus(oracleSid, oracleUser, oraclePasswd, oracleScript,'', '')


  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    

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

    objects = configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnEmpty(environment,'the variable CREATE_OBJECTS is not set.')

    defaultVersion=configReader.getValue('DEFAULT_VERSION')
    projectHelper.failOnEmpty(defaultVersion,'the variable DEFAULT_VERSION is not configured for this project.')

    version=parameterHelper.getParameterValue(['-v=','--version='],[])
    projectHelper.failOnEmpty(version,'no version was given')
    
    # find the versions
    versions=[]
    alterFolder=projectHelper.getAlterFolder()
    if projectHelper.folderPresent(alterFolder):
      versions=projectHelper.findFolders(alterFolder)
    createFolder=projectHelper.getCreateFolder()
    if projectHelper.folderPresent(createFolder):
      versions.append(defaultVersion)
    versionHelper=VersionHelper.VersionHelper(versions)
    versions=versionHelper.sort()
    
    version=version[0]
    projectHelper.failOnValueNotFound(versions,version,'the given version is not valid for this project.')
    
    projectHelper.failOnFolderNotPresent(ALTER_DIR+os.sep+version,'the update folder for this version is not present.')

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
    self.checkVersion(oracleSid,oracleUser,oraclePasswd,previousVersion,versionSelectStatement)
    self.checkEnvironment(oracleSid,oracleUser,oraclePasswd,environment,environmentSelectStatement)

    for scheme in schemes:

      print "updating scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)

      for object in objects:

        # global ddl objects
        folder=ALTER_DIR+os.sep+version+os.sep+scheme+os.sep+'ddl'+os.sep+object
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd)
      
        # environment specific ddl objects
        folder=ALTER_DIR+os.sep+version+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd)

      # global dat objects
      folder=ALTER_DIR+os.sep+version+os.sep+scheme+os.sep+'dat'
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd)

      # environment specific dat objects
      folder=ALTER_DIR+os.sep+version+os.sep+scheme+os.sep+'dat'+os.sep+environment
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd)
   
      print "scheme '"+scheme+"' updated."

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd)
        print "scheme '"+scheme+"' compiled."


