#!/usr/bin/env python
import core.MysqlPlugin as MysqlPlugin
import os
import subprocess
import core.NooraException as NooraException

class MysqlCreatePlugin(MysqlPlugin.MysqlPlugin):
  def __init__(self):
    MysqlPlugin.MysqlPlugin.__init__(self)
    self.setType("CREATE")

    self.addParameterDefinition('host',['-h','--host'])
    self.addParameterDefinition('database',['-s','-database'])
    self.addParameterDefinition('environment',['-e','--env'])
    

  def getDescription(self):
    return "executes the defined baseline scripts in the create folder."

  def getUsage(self):  
    print "NoOra database installer, MysqlCreatePlugin"
    print self.getDescription()
    print "-h= --host=      required contains the hostname of the mysql-server."
    print "-d= --database=  not required contains the database."
    print "-e= --env=       not required, used for mapping "
    print "                               the username and password."
    print "-nocompile       not required, disable the compilation of "
    print "                 packages, triggers and views."

  
  def getCreateDir(self):
    return self.getBaseDir()+os.sep+'create'


  def installComponent(self, url, mysqlHost, database, mysqlUser, mysqlPasswd):
    projectHelper=self.getProjectHelper()
    handle=open('feedback.log','wb')
    result=subprocess.call(['python',url+os.sep+'setup.py','-h='+mysqlHost,'-d='+database,'-u='+mysqlUser,'-p='+mysqlPasswd,'-silent'],shell=False,stdout=handle,stderr=handle)
    if result!=0:
      stream=projectHelper.readFile('feedback.log')
      raise NooraException.NooraException(stream)


  def installFiles(self, folder, mysqlHost, database, mysqlUser, mysqlPasswd, ignoreErrors):
    connector=self.getConnector()
    projectHelper=self.getProjectHelper()
    files=projectHelper.findFiles(folder)
    for file in files:
      url=folder+os.sep+file
      print url.split(self.getBaseDir())[1]
      if projectHelper.getFileExtension(file).lower()=='zip':
        projectHelper.extractFile(url)
        extractFolder=projectHelper.getFileRoot(url)
        self.installComponent(extractFolder,mysqlHost,database,mysqlUser,mysqlPasswd)
        projectHelper.removeFolderRecursive(extractFolder)
      elif projectHelper.getFileExtension(file).lower()=='mdl':
        pass
      else:
        connector.execute(mysqlHost, database, mysqlUser, mysqlPasswd, url, '', '', ignoreErrors)  


  def recompile(self, mysqlHost, database, mysqlUser, mysqlPasswd, ignoreErrors):
    connector=self.getConnector()
    mysqlScript=self.getScriptDir()+os.sep+'mysql_recompile.sql'
    connector.execute(mysqlHost, database, mysqlUser, mysqlPasswd, mysqlScript, '', '', ignoreErrors)
    

  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    
    
    ignoreErrors=False  
    if  parameterHelper.hasParameter('-ignore_errors')==True:
      ignoreErrors=True
    print ignoreErrors      

    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()

    mysqlHost=parameterHelper.getParameterValue(['-h=','--host='],[])
    projectHelper.failOnEmpty(mysqlHost,'no mysql host was given.')
    configReader.failOnValueNotFound('MYSQL_HOSTS',mysqlHost,'the given mysql host is not valid for this project.')
    mysqlHost=mysqlHost[0]
    
    databases=configReader.getValue('DATABASES')
    projectHelper.failOnNone(databases,'the variable DATABASES is not set.')
    databases=parameterHelper.getParameterValue(['-d=','--database='],databases)
    configReader.failOnValueNotFound('DATABASES',databases,'the given database is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    objects = configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnNone(objects,'the variable CREATE_OBJECTS is not set.')
    projectHelper.failOnEmpty(objects,'the variable CREATE_OBJECTS is not set.')

    for database in databases:
      print "creating database '"+database+"' in mysql-server '"+mysqlHost+"' using environment '"+environment+"'"
      mysqlUser=projectHelper.getMysqlUser(mysqlHost, database)
      mysqlPasswd=projectHelper.getMysqlPasswd(mysqlHost, database)
 
      for object in objects:  

        # global ddl objects
        folder=self.getCreateDir()+os.sep+database+os.sep+'ddl'+os.sep+object
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, mysqlHost, database, mysqlUser, mysqlPasswd, ignoreErrors)

        # environment specific ddl objects
        folder=self.getCreateDir()+os.sep+database+os.sep+'ddl'+os.sep+object+os.sep+environment
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, mysqlHost, database, mysqlUser, mysqlPasswd, ignoreErrors)

      # global dat objects
      folder=self.getCreateDir()+os.sep+database+os.sep+'dat'
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, mysqlHost, database, mysqlUser, mysqlPasswd, ignoreErrors)

      # environment specific dat objects
      folder=self.getCreateDir()+os.sep+database+os.sep+'dat'+os.sep+environment
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, mysqlHost, database, mysqlUser, mysqlPasswd, ignoreErrors)
    
      print "database '"+database+"' created."

    #if  parameterHelper.hasParameter('-nocompile')==False:
    #  for database in databases:
    #    print "compiling database '"+database+"' in mysql-server '"+mysqlHost+"' using environment '"+environment+"'"
    #    mysqlUser=projectHelper.getMysqlUser(mysqlHost, database)
    #    mysqlPasswd=projectHelper.getMysqlPasswd(mysqlHost, database)
    #    self.recompile(mysqlHost,database, mysqlUser, mysqlPasswd, ignoreErrors)
    #    print "scheme '"+database+"' compiled."


