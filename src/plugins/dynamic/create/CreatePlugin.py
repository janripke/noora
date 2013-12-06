#!/usr/bin/env python

import core.Plugin as Plugin
import os
import subprocess
import core.NooraException as NooraException
from connectors.SqlLoaderConnector import SqlLoaderConnector
from connectors.LoadJavaConnector import LoadJavaConnector

class CreatePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setSqlLoaderConnector(SqlLoaderConnector())
    self.setLoadJavaConnector(LoadJavaConnector())
    self.setType("CREATE")
    
    self.addParameterDefinition('database',['-s','-si','--sid'])
    self.addParameterDefinition('scheme',['-u','-sc','--scheme'])
    self.addParameterDefinition('environment',['-e','--env'])
    
  def setSqlLoaderConnector(self, connector):
    self.__sqlLoaderConnector = connector
  
  def getSqlLoaderConnector(self):
    return self.__sqlLoaderConnector
  
  def setLoadJavaConnector(self, connector):
    self.__loadJavaConnector = connector
    
  def getLoadJavaConnector(self):
    return self.__loadJavaConnector

  def getDescription(self):
    return "executes the defined baseline scripts in the create folder."

  def getUsage(self):  
    print "NoOra database installer, create.py"
    print self.getDescription()
    print "-s= --sid=     required contains the tnsname of the database."
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "               the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "               packages, triggers and views."

  
  def getCreateDir(self):
    return self.getBaseDir()+os.sep+'create'


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
      elif projectHelper.getFileExtension(file).lower()=='mdl':
        pass
      elif projectHelper.getFileExtension(file).lower()=='jar':
        loadJavaConnector = self.getLoadJavaConnector()
        loadJavaConnector.execute(oracleSid, oracleUser, oraclePasswd, url, '', '', ignoreErrors)  
      else:
        connector.execute(oracleSid, oracleUser, oraclePasswd, url, '', '', ignoreErrors)  


  def loadFiles(self, folder, oracleSid, oracleUser, oraclePasswd, ctlFile, ignoreErrors):   
    connector=self.getSqlLoaderConnector()
    projectHelper=self.getProjectHelper() 
    files=projectHelper.findFiles(folder)
    for file in files:
      url=folder+os.sep+file
      print url.split(self.getBaseDir())[1]
      if projectHelper.getFileExtension(file).lower()=='zip':
        projectHelper.extractFile(url,projectHelper.getFileRoot(file))
        
        for extractedFile in projectHelper.findFiles(folder+os.sep+projectHelper.getFileRoot(file)):
          connector.execute(oracleSid, oracleUser, oraclePasswd, ctlFile, extractedFile, ignoreErrors)
        projectHelper.removeFolderRecursive(folder+os.sep+projectHelper.getFileRoot(file))
      elif projectHelper.getFileExtension(file).lower()=='mdl':
        pass
      elif projectHelper.getFileExtension(file).lower()=='jar':
        loadJavaConnector = self.getLoadJavaConnector()
        loadJavaConnector.execute(oracleSid, oracleUser, oraclePasswd, url, '', '', ignoreErrors)        
      else:
        connector.execute(oracleSid, oracleUser, oraclePasswd, ctlFile, folder + os.sep + file, ignoreErrors)  



  def recompile(self, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getScriptDir()+os.sep+'recompile.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript, '', '', ignoreErrors)
    

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
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    objects = configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnNone(objects,'the variable CREATE_OBJECTS is not set.')
    projectHelper.failOnEmpty(objects,'the variable CREATE_OBJECTS is not set.')
    
    for scheme in schemes:
      print "creating scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
 
      for object in objects:  

        # global ddl objects
        folder=self.getCreateDir()+os.sep+scheme+os.sep+'ddl'+os.sep+object
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

        # environment specific ddl objects
        folder=self.getCreateDir()+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

      # global dat objects
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'dat'
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

      # environment specific dat objects
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'dat'+os.sep+environment
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)
        
      # global sqlldr files
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'sqlldr'
      if projectHelper.folderPresent(folder):
        ctlFolders = projectHelper.findFolders(folder)
        for ctlFolder in ctlFolders:
          ctlFile = folder+os.sep+ctlFolder+os.sep+ctlFolder+".ctl"
          self.loadFiles(folder+os.sep+ctlFolder, oracleSid, oracleUser, oraclePasswd, ctlFile, ignoreErrors)


      # environment sqlldr files
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'sqlldr'
      if projectHelper.folderPresent(folder):
        ctlFolders = projectHelper.findFolders(folder)
        for ctlFolder in ctlFolders:
          ctlFile = folder+os.sep+ctlFolder + os.sep + environment + os.sep + ctlFolder+ ".ctl"
          envFolder=folder + os.sep + ctlFolder + os.sep + environment
          if projectHelper.folderPresent(envFolder):          
            self.loadFiles(envFolder, oracleSid, oracleUser, oraclePasswd, ctlFile, ignoreErrors)

          
    
      print "scheme '"+scheme+"' created."

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd, ignoreErrors)
        print "scheme '"+scheme+"' compiled."


