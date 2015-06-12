#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"

sys.path.append(NOORA_DIR)

from core.ProjectHelper import ProjectHelper
from core.ConfigReader import ConfigReader
from core.VersionHelper import VersionHelper

class TestBase(unittest.TestCase): 
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
        

  def testVersionListPass(self):      

    #versions = ['2.10.0','2.10.0.1','2.10.0.2','2.10.1','3.0.0','2.9.2']
    
    versions = ['3.0.1.7', '3.1.0', '3.1.0.1', '3.1.0.2', '3.1.0.3', '3.1.0.4', '3.1.0.5', '3.1.1', '3.1.1.1', '3.1.1.10', '3.1.1.2', '3.1.1.3', '3.1.1.4', '3.1.1.5', '3.1.1.6', '3.1.1.7', '3.1.1.8', '3.1.1.9', '3.2.0', '3.2.1', '3.2.2']
    
    
    vh=VersionHelper(versions)
    sortedVersions = vh.sort()
    
    #self.assertEquals(options.size(),3, "invalid number of options") 
    self.assertEquals(sortedVersions, ['3.0.1.7', '3.1.0', '3.1.0.1', '3.1.0.2', '3.1.0.3', '3.1.0.4', '3.1.0.5', '3.1.1', '3.1.1.1',  '3.1.1.2', '3.1.1.3', '3.1.1.4', '3.1.1.5', '3.1.1.6', '3.1.1.7', '3.1.1.8', '3.1.1.9', '3.1.1.10', '3.2.0', '3.2.1', '3.2.2'], "invalid version order")    
    


if __name__=='__main__':
    unittest.main()    
#    versionHelper=VersionHelper.VersionHelper(versions)
#    versions=versionHelper.sort()

