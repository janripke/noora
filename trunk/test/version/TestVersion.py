#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"

sys.path.append(NOORA_DIR)

from org.noora.version.Versions import Versions
from org.noora.version.Version import Version
from core.VersionHelper import VersionHelper


class TestBase(unittest.TestCase): 
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
        

  def testVersionPass(self):    
    
    v = [[1,0,1],[1,0,0,1],[1,0,0,10],[1,0,0,2]]
    v.sort()
    #print v
    #vh = VersionHelper(v)
    #l = vh.sort()
    #return l
    
    v = [(1,0,1,None),(1,0,0,1),(1,0,0,10),(1,0,0,2)]
    print v
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