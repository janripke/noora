#!/usr/bin/env python
import os
from org.noora.plugin.Plugin import Plugin
from org.noora.io.File import File
from org.noora.io.Files import Files
from org.noora.io.Path import Path
from org.noora.plugin.mysql.update.UnknownVersionException import UnknownVersionException
from org.noora.plugin.mysql.update.InvalidEnvironmentException import InvalidEnvironmentException
from org.noora.plugin.mysql.update.InvalidVersionException import InvalidVersionException
from org.noora.version.Version import Version
from org.noora.version.Versions import Versions
from org.noora.version.VersionLoader import VersionLoader
from core.Property import FileReader
from org.noora.io.FileWriter import FileWriter
from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.version.VersionGuesser import VersionGuesser
from zipfile import ZipFile
import zipfile

class ReleasePlugin(Plugin):
  
  __revision__ = "$Revision: 334 $"
  
  def __init__(self):
    Plugin.__init__(self, "RELEASE", None)
    
  def getDescription(self):
    return "creates a database project archive."
  
  def getOptions(self, properties):
        
    options = Plugin.getOptions(self)
    options.addOption("-?", "--help", False, False,  "display help.")    
    options.addOption("-n", "--name", True, True, "name of the database project archive.")
    options.addOption("-v", "--version", True, True, "version of the database project.")
    
    return options
  



  def execute(self, commandLine, properties):
    name = commandLine.getOptionValue('-n')
    version = commandLine.getOptionValue('-v')
    current = properties.getPropertyValue('current.dir')
    
    versions = Versions()
    versionLoader = VersionLoader(versions)
    versionLoader.load(properties)
    versions.sort()  
    #print versions.list()
    versionGuesser=VersionGuesser(properties, versions)
    versionFolder = versionGuesser.toFolder(version)
    
    # create the target folder
    targetPath = Path.path(current, 'target')
    targetFile = File(targetPath)
    if not targetFile.exists():
      os.makedirs(targetPath)
    
    zipFilename = name+'_'+version+'.zip'
    zipHandle=ZipFile(targetPath+os.sep+zipFilename, 'w')
    
    
    files = Files.list(File(versionFolder), True)
    for file in files:      
      source = Path.path(file.getPath() ,file.getName())
      target = source.replace(current, '')
        
      
      zipHandle.write(source,target,zipfile.ZIP_DEFLATED)  
        
    print zipFilename + ' created.'    