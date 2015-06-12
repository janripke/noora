#!/usr/bin/env python
from org.noora.io.IOException import IOException

class Loadable:  
  def __init__(self):
    pass
  
  def load(self, fileReader = None):  
    raise IOException("method not implemented")
  

       


