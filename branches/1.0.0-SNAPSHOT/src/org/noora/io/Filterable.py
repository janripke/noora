#!/usr/bin/env python
from org.noora.io.IOException import IOException

class Filterable:
  def __init__(self):
    pass
    
  def accept(self, fileable):
    raise IOException("method not implemented")
       


