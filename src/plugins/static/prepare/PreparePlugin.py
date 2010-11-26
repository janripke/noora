#!/usr/bin/env python

import core.Plugin as Plugin
import core.VersionHelper as VersionHelper
import os


class PreparePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("PREPARE")


  def getUsage(self):  
    print "NoOra database installer, prepare.py"
    print "creates the folder structure for the given version"
    print "remarks : the given version must be present in config.VERSIONS"
    print "          the first version in config.VERSIONS is considered as the baseline (create)."
    print "          the folder structure is only created when the version folder is not already present."
    print "-v= --version= required, contains the version to create."
    print "-u= --scheme= --user=  not required, contains the scheme to create. "


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

    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()
    
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    versionScheme=configReader.getValue('VERSION_SCHEME')
    projectHelper.failOnEmpty(versionScheme,'the variable VERSION_SCHEME is not configured for this project.')

    versionInsertStatement=configReader.getValue('VERSION_INSERT_STATEMENT')
    projectHelper.failOnEmpty(versionInsertStatement,'the variable VERSION_INSERT_STATEMENT is not configured for this project.')

    versionUpdateStatement=configReader.getValue('VERSION_UPDATE_STATEMENT')
    projectHelper.failOnEmpty(versionUpdateStatement,'the variable VERSION_UPDATE_STATEMENT is not configured for this project.')

    environments=configReader.getValue('ENVIRONMENTS')
    projectHelper.failOnEmpty(environments,'the variable ENVIRONMENTS is not configured for this project.')

    defaultVersion=configReader.getValue('DEFAULT_VERSION')
    projectHelper.failOnEmpty(defaultVersion,'the variable DEFAULT_VERSION is not configured for this project.')
    version=parameterHelper.getParameterValue(['-v=','--version='],[])

    versions=configReader.getValue('VERSIONS')
    versionHelper=VersionHelper.VersionHelper(versions)

    if len(version)==0:
      version.append(versionHelper.getNextRevision(defaultVersion))

    if len(versions)==0:
      versions=version
    else:
      versions.append(version[0])
    
    version=version[0]
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

    # update or create the VERSION variable
    configReader.setValue('VERSIONS', versions)
    url=self.getBaseDir()+os.sep+'project.conf'
    configReader.saveToFile(url)

    print "version "+version+" created."


