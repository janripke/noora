#!/usr/bin/env python

import core.Plugin as Plugin
import core.VersionHelper as VersionHelper
import core.ConfigReader  as ConfigReader
import os


class GeneratePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("GENERATE")
    self.setBaseDir(os.path.abspath('.'))
    
    self.addParameterDefinition('project',['-pr','--project'])
    self.addParameterDefinition('database',['-si','--sid'])
    self.addParameterDefinition('scheme',['-sc','--scheme'])
    self.addParameterDefinition('username',['-u','--username'])
    self.addParameterDefinition('password',['-p','--password'])
    self.addParameterDefinition('version',['-v','--version'])
  
  def getPluginDir(self):
    return self.getNooraDir()+os.sep+'plugins'+os.sep+'dynamic'+os.sep+'generate'

  def getDescription(self):
    return "intiates a new NoOra database project, or a new release of an existing database project."
  

  def getUsage(self):  
    print "NoOra database installer, GeneratePlugin"
    print self.getDescription()
    print "-pr= --project=   not required, contains the database project name."
    print "-si= --sid=       not required, contains the oracle sid."
    print "-sc= --scheme=    not required, contains the scheme name."
    print "-u= --username=   not required, contains the username."
    print "-p= --password=   not required, contains the password."
    print "-v= --version=    required, contains the version to create."
    
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


  def getSqlVersionStatement(self, versions, version):
    configReader=self.getConfigReader()
    createVersion=versions[0]
    if createVersion==version: 
      stream=configReader.getValue('VERSION_INSERT_STATEMENT')
    else:
      stream=configReader.getValue('VERSION_UPDATE_STATEMENT')
      stream=stream.replace('<version>',version)
    return stream

  
  def getSqlEnvironmentStatement(self, environment):
    configReader=self.getConfigReader()
    stream=configReader.getValue('ENVIRONMENT_INSERT_STATEMENT')
    stream=stream.replace('<environment>',environment)
    return stream


  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    

    projectHelper=self.getProjectHelper()

    version=parameterHelper.getParameterValue(['-v=','--version='],[])

    if projectHelper.fileNotPresent('project.conf'):

      projectFolder=parameterHelper.getParameterValue(['-pr=','--project='],[])
      projectHelper.failOnEmpty(projectFolder,'no project is given, use the -pr= option')
      projectFolder=projectFolder[0]

      oracleSid=parameterHelper.getParameterValue(['-si=','--sid='],[])
      projectHelper.failOnEmpty(oracleSid,'no oracle sid is given, use the -si option')
      oracleSid=oracleSid[0]

      scheme=parameterHelper.getParameterValue(['-sc=','--scheme='],[])
      projectHelper.failOnEmpty(scheme,'no scheme is given, use the -sc option')
      scheme=scheme[0]

      oracleUser=parameterHelper.getParameterValue(['-u=','--username='],[])
      projectHelper.failOnEmpty(oracleUser,'no username is given, use the -u option')
      oracleUser=oracleUser[0]

      oraclePasswd=parameterHelper.getParameterValue(['-p=','--password='],[])
      projectHelper.failOnEmpty(oraclePasswd,'no username is given, use the -p option')
      oraclePasswd=oraclePasswd[0]
      
      projectHelper.failOnEmpty(version,'no version is given, use the -v option')

      projectHelper.failOnFolderPresent(projectFolder,'the given project is already present')

      # create the project folder
      os.makedirs(projectFolder)
      
      # create the project.conf file
      filename='project.conf'
      folder=self.getPluginDir()+os.sep+'templates'
      sourceFile=folder+os.sep+filename
      targetFile=projectFolder+os.sep+filename
      projectHelper.copyFile(sourceFile,targetFile)
      stream=projectHelper.readFile(targetFile)
      stream=stream.replace('<SID>',oracleSid)
      stream=stream.replace('<SCHEME>',scheme)
      stream=stream.replace('<USERNAME>',oracleUser)
      stream=stream.replace('<PASSWORD>',oraclePasswd)
      stream=stream.replace('<VERSION>',version[0])
      projectHelper.writeFile(targetFile,stream)

      os.chdir(projectFolder)
      self.setBaseDir(os.path.abspath('.'))
      projectHelper.setBaseDir(os.path.abspath('.'))

      print "project "+projectFolder+" created."
      
      
    configReader=ConfigReader.ConfigReader('project.conf')
    self.setConfigReader(configReader)
    projectHelper.setConfigReader(configReader)
    #configReader=self.getConfigReader()
    
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-sc=','--scheme='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    versionScheme=configReader.getValue('VERSION_SCHEME')
    projectHelper.failOnEmpty(versionScheme,'the variable VERSION_SCHEME is not configured for this project.')

    versionInsertStatement=configReader.getValue('VERSION_INSERT_STATEMENT')
    projectHelper.failOnEmpty(versionInsertStatement,'the variable VERSION_INSERT_STATEMENT is not configured for this project.')

    versionUpdateStatement=configReader.getValue('VERSION_UPDATE_STATEMENT')
    projectHelper.failOnEmpty(versionUpdateStatement,'the variable VERSION_UPDATE_STATEMENT is not configured for this project.')

    environments=configReader.getValue('ENVIRONMENTS')
    projectHelper.failOnEmpty(environments,'the variable ENVIRONMENTS is not configured for this project.')

    defaultVersion=self.getDefaultVersion()
    projectHelper.failOnEmpty(defaultVersion,'the variable DEFAULT_VERSION is not configured for this project.')


    # find the versions
    versions=self.getVersions(defaultVersion)
        
    if len(version)==0:
      versionHelper=VersionHelper.VersionHelper(versions)
      version.append(versionHelper.getNextRevision(defaultVersion))    
   
    version=version[0]
    
    if len(versions)==0:
      versions.append(defaultVersion)
    
    
    versionFolder=projectHelper.getBuildFolder(versions, version)
    projectHelper.failOnFolderPresent(versionFolder,'the given version is already present')

    objects=configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnNone(objects,'the variable CREATE_OBJECTS is not configured for this project.')

    # create the version folder
    os.makedirs(versionFolder)
  
    for scheme in schemes:

      # create the scheme folder
      schemeFolder=versionFolder+os.sep+scheme
      os.mkdir(schemeFolder)

      # create the dat folder
      datFolder=schemeFolder+os.sep+'dat'
      os.mkdir(datFolder)

      # create the version script in the dat folder
      if scheme==versionScheme:
        sqlScript=self.getSqlVersionStatement(versions, version)
        projectHelper.writeFile(datFolder+os.sep+'version.sql', sqlScript)

      # create the environment folders in the dat folder
      for environment in environments:
        os.mkdir(datFolder+os.sep+environment)

        # create the environment script in the dat folder.
        if scheme==versionScheme and versions[0]==version:
          sqlScript=self.getSqlEnvironmentStatement(environment)
          projectHelper.writeFile(datFolder+os.sep+environment+os.sep+'environment.sql', sqlScript)
                

      # create the ddl folder
      ddlFolder=schemeFolder+os.sep+'ddl'
      os.mkdir(ddlFolder)

      # create the object folders in the ddl folder
      for object in objects:
        os.mkdir(ddlFolder+os.sep+object)
      
      # create the template code on create.
      if scheme==versionScheme and versions[0]==version:
      
        files=projectHelper.findFiles(folder)
        for object in objects:
          folder=self.getPluginDir()+os.sep+'templates'+os.sep+object
          if projectHelper.folderPresent(folder):
            files=projectHelper.findFiles(folder)
            for file in files:
              sourceFile=folder+os.sep+file
              targetFile=ddlFolder+os.sep+object+os.sep+file
              projectHelper.copyFile(sourceFile,targetFile)

    print "version "+version+" created."

