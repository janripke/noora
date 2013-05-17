#!/usr/bin/env python
from org.noora.io.IOException import IOException

class Fileable:
  def __init__(self, pathName=None):
    pass
    
  @staticmethod
  def pathSeperator(self):
    raise IOException("method not implemented")
  
  def exists(self):
    raise IOException("method not implemented")
  
  def notExists(self):
    raise IOException("method not implemented")
  
  def isFile(self):
    raise IOException("method not implemented")
  
  def isDirectory(self):
    raise IOException("method not implemented")
  
  def getName(self):
    raise IOException("method not implemented")
  
  def getPath(self):
    raise IOException("method not implemented")
  
  def getExtension(self):
    raise IOException("method not implemented")
  
  def getRoot(self):
    raise IOException("method not implemented")
  
  def delete(self,recursive=False):
    raise IOException("method not implemented")


       


