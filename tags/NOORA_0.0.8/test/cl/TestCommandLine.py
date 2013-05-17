#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)



from org.noora.cl.Parser import Parser
from org.noora.cl.Options import Options
from org.noora.cl.MissingOptionException import MissingOptionException
from org.noora.cl.MissingArgumentException import MissingArgumentException
from org.noora.cl.UnrecognizedOptionException import UnrecognizedOptionException
from org.noora.cl.UnrecognizedArgumentException import UnrecognizedArgumentException

class TestParameters(unittest.TestCase):      

  def setUp(self):
    pass

  def tearDown(self):
    pass

      
  def testOptions(self):
    options = Options()
    options.addOption("-?","--help", False, False,  "display help")      
    options.addOption("-s","--sid", True, True, "tnsname (sid) of the database.")
    options.addOption("-u","--user", True, False, "scheme (user) of the database.")
    self.assertEquals(options.size(),3, "invalid number of options")
    parser = Parser()
    commandLine = parser.parse(options,['-s=orcl','--user=apps'])
    
    self.assertEquals(commandLine.hasOption('-s'), True, "invalid parameter")
    self.assertEquals(commandLine.hasOption('-?'), False, "invalid parameter")
    self.assertEquals(commandLine.hasOption('-t'), False, "invalid parameter")
    self.assertEquals(commandLine.hasOption('-u'), True, "invalid parameter")
    self.assertEquals(commandLine.getOptionValues('-s'), ['orcl'], "invalid option value")
    self.assertEquals(commandLine.getOptionValue('-s'), 'orcl', "invalid option value")
    self.assertEquals(commandLine.getOptionValue('-s'), 'orcl', "invalid option value")
    
  
  def testMissingOptionException(self):
    
    options = Options()
    options.addOption("-?","--help", False, False,  "display help")      
    options.addOption("-s","--sid", True, True, "tnsname (sid) of the database.")
    options.addOption("-u","--user", True, True, "scheme (user) of the database.")
    parser = Parser()
    commandLine = parser.parse(options,['-s=orcl'])
 
    try:
      parser.checkRequiredOptions()
    except MissingOptionException as moe:
      self.assertEquals(moe.getMessage(), 'missing option -u')

  def testMissingArgument(self):
    options = Options()
    options.addOption("-?","--help", False, False,  "display help")      
    options.addOption("-s","--sid", True, True, "tnsname (sid) of the database.")
    options.addOption("-u","--user", True, True, "scheme (user) of the database.")
    parser = Parser()
    commandLine = parser.parse(options,['-s'])
    
    try:
      parser.checkRequiredArguments()
    except MissingArgumentException as mae:
      self.assertEquals(mae.getMessage(), 'missing argument in option -s')
    
  def testUnrecognizedOption(self):
    options = Options()
    options.addOption("-?","--help", False, False,  "display help")      
    options.addOption("-s","--sid", True, True, "tnsname (sid) of the database.")
    options.addOption("-u","--user", True, True, "scheme (user) of the database.")
    parser = Parser()
        
    try:
      commandLine = parser.parse(options,['-q'])
    except UnrecognizedOptionException as uoe:
      self.assertEquals(uoe.getMessage(), 'unrecognized option -q')
    
  def testMissingArgumentValue(self):
    options = Options()
    options.addOption("-?","--help", False, False,  "display help")      
    options.addOption("-s","--sid", True, True, "tnsname (sid) of the database.")
    options.addOption("-u","--user", True, True, "scheme (user) of the database.")
    option = options.getOption("-s")
    option.setValues(['localhost'])
    parser = Parser()
    
    
    
    try:
      commandLine = parser.parse(options,['-s=orcl'])
      parser.checkRequiredArguments()
    except UnrecognizedArgumentException as uae:
      self.assertEquals(uae.getMessage(), 'unrecognized argument orcl')
 

 
    #self.assertEquals(commandLine('-u'), True, "invalid parameter")

if __name__ == '__main__':
    unittest.main()
