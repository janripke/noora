import unittest
import os
from zipfile import ZipFile
import zipfile
from org.noora.io.File import File
from org.noora.io.Files import Files
from org.noora.io.Path import Path
from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.io.FileReader import FileReader
from org.noora.io.Filters import Filters
from org.noora.io.FileFolderFilter import FileFolderFilter
from org.noora.version.Versions import Versions
from org.noora.version.VersionLoader import VersionLoader
from org.noora.version.VersionGuesser import VersionGuesser

class TestBase(unittest.TestCase): 
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
        

  def testZipPass(self):    



    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        
    file = File("myproject.conf")
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)


    properties.setProperty("current.dir", os.path.abspath('.'))
    properties.setProperty("alter.dir",properties.getPropertyValue("current.dir")+os.sep+"alter")
    properties.setProperty("create.dir",properties.getPropertyValue("current.dir")+os.sep+"create")

    

    versions = Versions()
    versionLoader = VersionLoader(versions)
    versionLoader.load(properties)
    versions.sort()  
    #print versions.list()
    versionGuesser=VersionGuesser(properties, versions)
    version = versionGuesser.toFolder('1.0.0')
    
    currentFile = File(os.path.abspath('.'))
    current = Path.path(currentFile.getPath() ,currentFile.getName())
    
    targetPath = Path.path(current,'target')
    targetFile = File(targetPath)
    if not targetFile.exists():
      os.makedirs(targetPath)
 
    
    zipHandle=ZipFile(targetPath+os.sep+'example_'+version+'.zip', 'w')
    
    excludedFolders = properties.getPropertyValues('EXCLUDED_FOLDERS')
    
    files = Files.list(currentFile, True)
    
    filters = Filters()
        
    excludedFolders=properties.getPropertyValues('EXCLUDED_FOLDERS')            
    for excludedFolder in excludedFolders:
      ef = File(excludedFolder)
      ff = FileFolderFilter(ef)
      filters.add(ff)

    
    
    
    for file in files:
      
      result = False
      for excludedFolder in excludedFolders:
        if excludedFolder in file.getPath()+file.getName():
          result = True
          break
      
      #if filters.accept(file)==False:  
      if not result:
        source = Path.path(file.getPath() ,file.getName())
        target = source.replace(current, '')
        print file.getPath() ,file.getName()
      
        zipHandle.write(source,target,zipfile.ZIP_DEFLATED)
       

if __name__=='__main__':
    unittest.main()