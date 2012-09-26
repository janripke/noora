#!/usr/bin/env python

from org.noora.parser.ParserException import ParserException

class Parsable():
  def __init__(self):
    pass
    
  def parse(self):
    raise ParserException("method not implemented")
 
