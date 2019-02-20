#!/usr/bin/env python
from org.noora.cl.ParseException import ParseException

class Parseable:
  def __init__(self):
    pass
  
  def checkRequiredOptions(self):
    raise ParseException("method not implemented")
    
  def parse(self, options=None, arguments=None): 
    raise ParseException("method not implemented")