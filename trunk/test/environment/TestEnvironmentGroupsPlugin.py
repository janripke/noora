#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'


sys.path.append(NOORA_DIR)
sys.path.append(PLUGIN_DIR)

from core.ConfigReader import ConfigReader

M_LF         = chr(10)

class TestBase(unittest.TestCase):
    
  def testEnvironmentGroup(self):
    configReader = ConfigReader('project.conf')
    environmentGroups=configReader.getValue('ENVIRONMENT_GROUPS')
    environment = 'dev'
    
    
    groups = []
    if environmentGroups:
      for environmentGroup in environmentGroups:
        # print environmentGroup
        group = environmentGroup[0]
        environments = environmentGroup[1]
        # print group, environments
        if environment.lower() in environments:
          groups.append(group)
    print groups 

if __name__=='__main__':
    unittest.main()