#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"

sys.path.append(NOORA_DIR)

from org.noora.version.Versions import Versions
from core.VersionHelper import VersionHelper

from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.io.File import File
from org.noora.io.Files import Files
from org.noora.io.FileReader import FileReader

from org.noora.version.Version import Version
from org.noora.version.VersionLoader import VersionLoader   
    

class TestBase(unittest.TestCase): 
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
  
  def testVersionLoader(self):
    
    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        

    file = File("myproject.conf")
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)
    
    properties.setProperty("current.dir", os.path.abspath('.'))
    properties.setProperty("project.file", "myproject.conf")
    properties.setProperty("alter.dir",properties.getPropertyValue("current.dir")+os.sep+"alter")
    properties.setProperty("create.dir",properties.getPropertyValue("current.dir")+os.sep+"create")
    print "current.dir",properties.getPropertyValue("current.dir")
    print "alter.dir",properties.getPropertyValue("alter.dir")
    print "default_version", properties.getPropertyValues("DEFAULT_VERSION")
    
    
    # a File object is not a Version object
    # 
    versions = Versions()
    versionLoader = VersionLoader(versions)
    versionLoader.load(properties)
    versions.sort()
    #versions.sort()
    #print "versions",versions.getVersions()
    v = Version('1.0.1')
    print versions.previous(v).getValue()
    
    #versions=[]
    #alterFolder=projectHelper.getAlterFolder()
    #if projectHelper.folderPresent(alterFolder):
    #  versions=projectHelper.findFolders(alterFolder)
    #createFolder=projectHelper.getCreateFolder()
    #if projectHelper.folderPresent(createFolder):
    #  versions.append(defaultVersion)
   
    #versionHelper=VersionHelper.VersionHelper(versions)
    #versions=versionHelper.sort()
    #versions.sort()    
    #return versions
  
  def versions(self):
    versions = Versions()
    v = Version(1,0,0)
    versions.add(v)
    v = Version(10,0,0)
    versions.add(v)
    v = Version(2,0,0)
    versions.add(v)
    v = Version(10,0,0,1)
    versions.add(v)
    
    versions.sort()
    for version in versions.getVersions():
      print version.getMajor(), version.getMinor(), version.getRevision(),version.getPatch()
            

  def testVersionListPass(self):
    v = [[2,10,0], [2,7,2,4], [2,8,0], [2,8,0,1], [2,8,0,2], [2,9,0]]
    v.sort()
    print v[0]


  def versionPass(self):    
    
    v = [[1,0,1],[1,0,0,1],[1,0,0,10],[1,0,0,2]]
    v.sort()
    #print v
    #vh = VersionHelper(v)
    #l = vh.sort()
    #return l
    
    v = [(1,0,1,None),(1,0,0,1),(1,0,0,10),(1,0,0,2)]
    #print v
    v.sort()
    print v
        
    
    versions = Versions()
    versions.addVersion(1, 0, 1)
    versions.addVersion(1, 0, 0, 1)
    versions.addVersion(1, 0, 0, 10)
    versions.addVersion(1, 0, 0, 2)
    versions.sort()    

    vl= versions.getVersions()
    for version in vl:
      print version.list()
      
    v = Version(1,0,0,10)
    pv = versions.previousVersion(v)
    if pv: print pv.list()
    lv = versions.lastVersion()  
    if lv: print lv.list()
    #versions.addVersion(1, 0, 0, 1)
    #versions.addVersion(1, 0, 0, 10)
    #versions.addVersion(1, 0, 0, 2)    
    #versions.sort()    
    #print versions.lastVersion().list()
    #print versions.getVersions()

if __name__=='__main__':
    unittest.main()