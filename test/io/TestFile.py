#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from org.noora.io.File import File
from org.noora.io.Files import Files
from org.noora.io.FileFilter import FileFilter
from org.noora.io.FileExtensionFilter import FileExtensionFilter
from org.noora.io.FileFolderFilter import FileFolderFilter
from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.io.FileReader import FileReader
from org.noora.io.Filters import Filters
from org.noora.io.FolderFilterLoader import FolderFilterLoader
from org.noora.io.PropertyProvider import FileFormatAdapter

class TestFile(unittest.TestCase):  

  def setUp(self):
    pass

  def tearDown(self):
    pass

      
  def testFile(self):
    file = File('project.conf')
    self.assertEquals(file.isFile(), True, "is a file expected")
    self.assertEquals(file.isDirectory(), False, "is not a directory expected")
    self.assertEquals(file.getName(), 'project.conf', "invalid name") 
    self.assertEquals(file.getPath(), '', "invalid path") 

  def testListFiles(self):
    
    folder = File(NOORA_DIR + os.sep + 'org'+os.sep+'noora'+os.sep+'plugin'+os.sep+'mysql'+os.sep+'drop')
    files = Files.list(file=folder, recursive=True)   
   
  def testFileFilter(self):
    
    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        
    file = File("project.conf")
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)
    
    excludedFiles=properties.getPropertyValues('EXCLUDED_FILES')
    self.assertEquals(excludedFiles, ['install.sql'], "install.sql expected")
    
    # install.sql is an excluded file.
    filters = Filters()
    for excludedFile in excludedFiles:
      ef = File(excludedFile)
      ff = FileFilter(ef)
      filters.add(ff)    
    
    file = File('test.sql')
    self.assertEquals(filters.accept(file), False, "test.sql is in filter.")
    
    file = File('install.sql')
    self.assertEquals(filters.accept(file), True, "install.sql is not in filter.")
    
  def testFileExtensionFilter(self):
    
    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        
    file = File("project.conf")
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)

    
    excludedExtensions=properties.getPropertyValues('EXCLUDED_EXTENSIONS')
    self.assertEquals(excludedExtensions, ['bak', '~', 'pyc', 'log'], "'bak', '~', 'pyc', 'log' expected")
    
    filters = Filters()
    for excludedExtension in excludedExtensions:
      ef = File("*."+ excludedExtension)
      ff = FileExtensionFilter(ef)
      filters.add(ff)
          
    file = File('install.sql')  
    self.assertEquals(filters.accept(file), False, "install.sql is in filter.")
        
    file = File('install.pyc')
    self.assertEquals(filters.accept(file), True, "install.pyc is not in filter.")
    

  def testFileFolderFilter(self):
    
    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        
    file = File("project.conf")
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)

    
    excludedFolders=properties.getPropertyValues('EXCLUDED_FOLDERS')    
    self.assertEquals(excludedFolders, ['.svn', 'hotfix'], "'.svn', 'hotfix' expected")

    filters = Filters()
    for excludedFolder in excludedFolders:
      ef = File(excludedFolder)
      ff = FileFolderFilter(ef)
      filters.add(ff)
    file = File(NOORA_DIR+os.sep+'org/noora/plugin/mysql/drop/.svn')
    self.assertEquals(filters.accept(file), True, ".svn is in filter.")    
    file = File('.svn')
    self.assertEquals(filters.accept(file), True, ".svn is in filter.")  
    
    
    
    

if __name__ == '__main__':
    unittest.main()