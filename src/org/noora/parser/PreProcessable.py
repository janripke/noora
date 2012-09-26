#!/usr/bin/env python
from org.noora.parser.ParserException import ParserException

class PreProcessable:
  def __init__(self):
    pass

  def parse(self, parsable=None):
    raise ParserException("method not implemented")


