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

class BuildPlugin(Plugin):
  
  __revision__ = "$Revision: 334 $"
  
  def __init__(self):
    Plugin.__init__(self, "BUILD", None)
    
  def getDescription(self):
    return "creates a database independend component."
  
  def getOptions(self, properties):
        
    options = Plugin.getOptions(self)
    options.addOption("-?", "--help", False, False,  "display help")
    
    options.addOption("-v", "--version", True, True,  "version of the database project.")
    
    return options
  



  def execute(self, commandLine, properties):
    pass    