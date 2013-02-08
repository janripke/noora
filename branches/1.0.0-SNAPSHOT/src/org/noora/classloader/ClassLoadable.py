#!/usr/bin/env python
from org.noora.classloader.ClassLoaderException import ClassLoaderException


class ClassLoadable:
    
  def __init__(self):
    pass
    
  def find(self, moduleName, className):
    raise ClassLoaderException("method not implemented") 
    
  def findByPattern(self, pattern):
    raise ClassLoaderException("method not implemented")
    
   
        
