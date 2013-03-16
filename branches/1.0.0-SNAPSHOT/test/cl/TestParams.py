#!/usr/bin/env python

from org.noora.app.Params import Params
from org.noora.app.Params import PluginParameter
from org.noora.app.Params import OptionParameter
from org.noora.app.Params import ArgParameter

import os
import sys
import unittest

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)




class TestParameters(unittest.TestCase):      

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testParams(self):
    params = Params(["help", "recreate"])
    plugins = params.getPluginParams()
    self.assertEqual(len(plugins), 2, "invalid number of plugins (got {0}, 2 expected".format(len(plugins)))
    
    params = Params(["recreate", "-e", "dev", "-v"])
    plugins = params.getPluginParams()
    self.assertEqual(len(plugins),1,"invalid number of plugins")
    self.assertEqual(plugins[0].getName(),"recreate","invalid plugin argument (got {0}, recreate expected)".format(plugins[0]))
    args = params.getArgParams()
    self.assertEqual(len(args),1,"invalid number of arguments (-e dev)")
    self.assertEqual(args[0].getName(),"-e","invalid switch for argument (-e dev), -e not found")   
    self.assertEqual(args[0].getValue(),"dev","invalid arg for argument (-e dev), dev not found")
    options = params.getOptionParams()
    self.assertEqual(len(options),1,"invalid number of options (-v)")
    self.assertEqual(options[0].getName(),"-v","invalid switch for option (-v), -v not found")   
    
    params = Params(["recreate", "-v", "-e", "dev"])
    plugins = params.getPluginParams()
    self.assertEqual(len(plugins),1,"invalid number of plugins")
    self.assertEqual(plugins[0].getName(),"recreate","invalid plugin argument (got {0}, recreate expected)".format(plugins[0]))
    args = params.getArgParams()
    self.assertEqual(len(args),1,"invalid number of arguments (-e dev)")
    self.assertEqual(args[0].getName(),"-e","invalid switch for argument (-e dev), -e not found")   
    self.assertEqual(args[0].getValue(),"dev","invalid arg for argument (-e dev), dev not found")
    options = params.getOptionParams()
    self.assertEqual(len(options),1,"invalid number of options (-v)")
    self.assertEqual(options[0].getName(),"-v","invalid switch for option (-v), -v not found")
    
    params = Params(["recreate", "-e", "-v", "dev"])
    plugins = params.getPluginParams()
    self.assertEqual(len(plugins),1,"invalid number of plugins")
    self.assertEqual(plugins[0].getName(),"recreate","invalid plugin argument (got {0}, recreate expected)".format(plugins[0]))
    args = params.getArgParams()
    self.assertEqual(len(args),1,"invalid number of arguments (-v dev)")
    self.assertEqual(args[0].getName(),"-v","invalid switch for argument (-v dev), -v not found")   
    self.assertEqual(args[0].getValue(),"dev","invalid arg for argument (-v dev), dev not found")
    options = params.getOptionParams()
    self.assertEqual(len(options),1,"invalid number of options (-v)")
    self.assertEqual(options[0].getName(),"-e","invalid switch for option (-e), -e not found")

    params = Params(["recreate", "-v", "-e=dev", "--connector=mysql-dev"])
    plugins = params.getPluginParams()
    self.assertEqual(len(plugins),1,"invalid number of plugins")
    self.assertEqual(plugins[0].getName(),"recreate","invalid plugin argument (got {0}, recreate expected)".format(plugins[0]))
    args = params.getArgParams()
    self.assertEqual(len(args),2,"invalid number of arguments (-v dev)")
    self.assertEqual(args[0].getName(),"-e","invalid switch for argument (-e dev), -e not found")   
    self.assertEqual(args[0].getValue(),"dev","invalid arg for argument (-e dev), dev not found")
    self.assertEqual(args[1].getName(),"--connector","invalid switch for argument (--connector=mysql-dev), --connector not found")   
    self.assertEqual(args[1].getValue(),"mysql-dev","invalid arg for argument (--connector=mysql-dev), mysql-dev not found")
    options = params.getOptionParams()
    self.assertEqual(len(options),1,"invalid number of options (-v)")
    self.assertEqual(options[0].getName(),"-v","invalid switch for option (-v), -v not found")
    
    
if __name__ == '__main__':
    unittest.main()
