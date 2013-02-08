#!/usr/bin/env python
from org.noora.cl.Option import Option

class OptionFactory:
  def __init__(self):
    pass
  
  @staticmethod
  def newOption(type=None, longType=None, hasArguments=False, required=False, description=None):
    return Option(type, longType, hasArguments, required, description)
