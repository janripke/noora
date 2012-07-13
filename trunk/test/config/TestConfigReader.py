#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"
EXAMPLE_DIR = NOORA_DIR + os.sep + 'examples'
PROJECT_DIR = EXAMPLE_DIR + os.sep + 'project-db'


sys.path.append(NOORA_DIR)
import core.ProjectHelper   as ProjectHelper
import core.ConfigReader    as ConfigReader


class TestConfigReader(unittest.TestCase):
    
   
        
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
    
  def testConfigReaderPass(self):
    projectHelper = ProjectHelper.ProjectHelper("")
    projectHelper.setNooraDir(NOORA_DIR)
    print projectHelper.findTemplateFile('project.conf')
    print sys.argv[0]
    print os.path.abspath(os.path.dirname(sys.argv[0]))
    config = ConfigReader.ConfigReader(projectHelper.findTemplateFile('project.conf'))
  


if __name__ == '__main__':
    unittest.main()
