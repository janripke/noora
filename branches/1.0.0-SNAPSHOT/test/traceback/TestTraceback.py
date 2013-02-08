#!/usr/bin/env python

import unittest
import sys, traceback

from org.noora.processor.ProcessorException import ProcessorException

class MyError(Exception):
  def __init__(self, value, e):
    print e
    self.value = value
    self.exception = e
  def __str__(self):
    return repr(self.value, self.exception)

class TestTraceback(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProcessor(self):


      try:
        raise ProcessorException('Error in processor')
      except  Exception as e:
        print e
        type_, value_, traceback_ = sys.exc_info()
        ex = traceback.format_exception(type_, value_, traceback_)
        print ex
        traceback.print_exc(file=sys.stdout)
        raise MyError("Error in myError",e)
      

      
      try:
        result = 10.0 / 0.0 
      except:
        type_, value_, traceback_ = sys.exc_info()
        ex = traceback.format_exception(type_, value_, traceback_)
        print ex
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

  
    
            
  
      


if __name__ == '__main__':
    unittest.main()
