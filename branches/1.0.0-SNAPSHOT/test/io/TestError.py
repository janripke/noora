#!/usr/bin/env python

import os
import sys
import unittest
from org.noora.io.NoOraError import NoOraError

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

class TestError(unittest.TestCase):
  
  def setUp(self):
    pass

  def tearDown(self):
    pass
  
  def raiseException(self, excep):
    try:
      raise excep.addReason("key3", "value3")
    except NoOraError as e:
      raise e.addReason("key4", "value4")
    
  def testError(self):
    excep = None
    
    try:
      raise NoOraError("key1", "value1")
    except NoOraError as e:
      excep = e
      
    print excep.getReasons()
      
    try:
      self.raiseException(excep)
    except NoOraError as e:
      print e.getReasons()
    
