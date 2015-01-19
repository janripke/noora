#!/usr/bin/env python

import os
from org.noora.io.Files import Files
from org.noora.io.File import File
from org.noora.io.Filters import Filters
from org.noora.io.FileFolderFilter import FileFolderFilter
from org.noora.io.FileExtensionFilter import FileExtensionFilter
from org.noora.io.FileFilter import FileFilter

class ConnectionExecutor:
  def __init__(self):
    pass
  
  @staticmethod
  def execute(connector, executor, properties, folder):
    filters = Filters()
        
    excludedFolders=properties.getPropertyValues('EXCLUDED_FOLDERS')            
    for excludedFolder in excludedFolders:
      ef = File(excludedFolder)
      ff = FileFolderFilter(ef)
      filters.add(ff)
          
    excludedExtensions=properties.getPropertyValues('EXCLUDED_EXTENSIONS')
    for excludedExtension in excludedExtensions:
      ef = File("*."+ excludedExtension)
      ff = FileExtensionFilter(ef)
      filters.add(ff)

    excludedFiles=properties.getPropertyValues('EXCLUDED_FILES')
    for excludedFile in excludedFiles:
      ef = File(excludedFile)
      ff = FileFilter(ef)
      filters.add(ff)  
    
    if folder.isDirectory():
      files = Files.list(folder)           
      for file in files:              
        if filters.accept(file)==False and file.isDirectory()==False:  
          url = file.getPath()+os.sep+file.getName()        
          print url
        
#          executor = ExecuteFactory.newMysqlExecute()
#          executor.setHost(host)
#          executor.setDatabase(database)
#          executor.setIgnoreErrors(ignoreErrors)
#          executor.setUsername(user)
#          executor.setPassword(passwd)
          executor.setScript(file)
        
          connector.execute(executor, properties)
