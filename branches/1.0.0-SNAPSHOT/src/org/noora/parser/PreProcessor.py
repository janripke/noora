#!/usr/bin/env python

from org.noora.parser.PreProcessable import PreProcessable

class PreProcessor(PreProcessable):
  def __init__(self):
    PreProcessable.__init__(self)
  
  def parse(self, parsable=None):
    return parsable.parse()

