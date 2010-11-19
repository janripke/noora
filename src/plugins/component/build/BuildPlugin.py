#!/usr/bin/env python

import core.Plugin as Plugin
import core.VersionHelper as VersionHelper
import os
import sys
import zipfile

M_LF         = chr(10)
M_QUOTE      = chr(39)

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR     = os.path.abspath('.')
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'+os.sep+'component'+os.sep+'build'

class BuildPlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("BUILD")

  def getUsage(self):
    print "NoOra database installer, build.py"
    print "creates a database independend component."
    print "-v= --verion=  required, the version to build"


  def isFileExcluded(self, filename):
    configReader=self.getConfigReader()
    excludedFiles=configReader.getValue('COMPONENT_EXCLUDED_FILES')
    for excludedFile in excludedFiles:
      if filename.lower()==excludedFile.lower():
        return True

  def getSqlVersionStatement(self, versions, version, componentName):
    configReader=self.getConfigReader()
    createVersion=versions[0]
    if createVersion==version:
      stream=configReader.getValue('COMPONENT_INSERT_STATEMENT')
    else:
      stream=configReader.getValue('COMPONENT_UPDATE_STATEMENT')
    stream=stream.replace('<version>',version)
    stream=stream.replace('<name>',componentName)
    return stream


  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)

    projectHelper=self.getProjectHelper()
    configReader=self.getConfigReader()

    version=parameterHelper.getParameterValue(['-v=','--version='],[])
    projectHelper.failOnEmpty(version,'no version was given')

    defaultVersion = configReader.getValue('DEFAULT_VERSION')
    projectHelper.failOnNone(defaultVersion,'the variable DEFAULT_VERSION is not set.')

    componentName=configReader.getValue('COMPONENT_NAME')
    projectHelper.failOnNone(componentName,'the variable COMPONENT_NAME is not set.')

    componentSelectStatement=configReader.getValue('COMPONENT_SELECT_STATEMENT')
    projectHelper.failOnNone(componentSelectStatement,'the variable COMPONENT_SELECT_STATEMENT is not set.')


    componentTargetFolder=configReader.getValue('COMPONENT_TARGET_FOLDER')
    projectHelper.failOnNone(componentTargetFolder,'the variable COMPONENT_TARGET_FOLDER is not set.')
    targetFolder = BASE_DIR + os.sep + componentTargetFolder

    componentExcludedFiles=configReader.getValue('COMPONENT_EXCLUDED_FILES')
    projectHelper.failOnNone(componentExcludedFiles,'the variable COMPONENT_EXCLUDED_FILES is not set.')
        
    schemes=configReader.getValue('SCHEMES')
    projectHelper.failOnNone(schemes,'the variable SCHEMES is not set.')
        
    objects = configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnNone(schemes,'the variable CREATE_OBJECTS is not set.')


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

    buildFolder=projectHelper.getBuildFolder(versions, version)
    projectHelper.invalidBuildFolder(buildFolder)

    print "building component with version '"+version+"'"

    # compress the build
    if projectHelper.folderNotPresent(targetFolder):
      os.makedirs(targetFolder)
  
    zipUrl=targetFolder + os.sep + componentName + '_' + version + '.zip'
    zipHandle=zipfile.ZipFile(zipUrl,'w')

    for scheme in schemes:

      for object in objects:

        # global ddl objects
        folder=buildFolder+os.sep+scheme+os.sep+'ddl'+os.sep+object
        zipFolder=componentName + '_' + version + os.sep + 'ddl' + os.sep + object + os.sep
        if projectHelper.folderPresent(folder):
          if folder.endswith('lib')==False:
            files=projectHelper.findFiles(folder)
            for file in files:
              sourceFile=folder+os.sep+file
              targetFile=zipFolder+file
              zipHandle.write(sourceFile,targetFile,zipfile.ZIP_DEFLATED)

  
      # global dat files
      folder=buildFolder+os.sep+scheme+os.sep+'dat'
      zipFolder=componentName+'_'+version+os.sep+'dat'+os.sep
      
      if projectHelper.folderPresent(folder):
        files=projectHelper.findFiles(folder)
        for file in files:
          if self.isFileExcluded(file)==False:
            sourceFile=folder+os.sep+file
            targetFile=zipFolder+file
            zipHandle.write(sourceFile,targetFile,zipfile.ZIP_DEFLATED)

    # create the version script in the dat folder      
    stream=self.getSqlVersionStatement(versions, version, componentName)
    filename="version.sql"
    sourceFile=targetFolder+os.sep+filename
    projectHelper.writeFile(sourceFile,stream)

    zipFolder=componentName+'_'+version+os.sep+'dat'+os.sep
    targetFile=zipFolder+filename

    zipHandle.write(sourceFile,targetFile,zipfile.ZIP_DEFLATED)
    os.remove(sourceFile)

    

    # add template files
    folder=PLUGIN_DIR+os.sep+'templates'
    zipFolder=componentName+'_'+version+os.sep
    if projectHelper.folderPresent(folder):
      files=projectHelper.findFiles(folder)
      for file in files:
        sourceFile=folder+os.sep+file
        targetFile=zipFolder+file
        zipHandle.write(sourceFile,targetFile,zipfile.ZIP_DEFLATED)

    # create and add component.conf
    filename="component.conf"
    sourceFile=targetFolder+os.sep+filename

    lines=[]
    lines.append('COMPONENT_NAME='+M_QUOTE+componentName+M_QUOTE)
    lines.append('COMPONENT_VERSION='+M_QUOTE+version+M_QUOTE)
    lines.append('COMPONENT_SELECT_STATEMENT='+'"'+componentSelectStatement+'"')
    lines.append('COMPONENT_VERSIONS='+str(versions))
    stream = M_LF.join(lines)
    stream=stream.replace('<name>',componentName)
    projectHelper.writeFile(sourceFile,stream)

    zipFolder=componentName+'_'+version+os.sep
    targetFile=zipFolder+filename

    zipHandle.write(sourceFile,targetFile,zipfile.ZIP_DEFLATED)
    os.remove(sourceFile)

    zipHandle.close()
    print "component for version "+version+" created."

