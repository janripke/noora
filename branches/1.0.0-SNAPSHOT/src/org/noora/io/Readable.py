#!/usr/bin/env python
from org.noora.io.IOException import IOException

class Readable:
  
  def __init__(self):
    pass
  
  def read(self):  
    raise IOException("method not implemented")
  
  def close(self):
    raise IOException("method not implemented")
  
  

       


