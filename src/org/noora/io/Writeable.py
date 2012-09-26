#!/usr/bin/env python
from org.noora.io.IOException import IOException

class Writeable:
  
  def __init__(self):
    pass
  
  def fileno(self):
    raise IOException("method not implemented")
  
  def write(self, buffer):  
    raise IOException("method not implemented")
  
  def close(self):
    raise IOException("method not implemented")



       


