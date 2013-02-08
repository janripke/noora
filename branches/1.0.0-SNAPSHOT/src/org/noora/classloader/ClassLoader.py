#!/usr/bin/env python
from org.noora.classloader.ClassLoadable import ClassLoadable
from org.noora.classloader.ClassLoaderException import ClassLoaderException
import sys

class ClassLoader(ClassLoadable):
    
  def __init__(self):
    ClassLoadable.__init__(self)    
    
  def find(self, moduleName,className):
    try:
      mod = __import__(moduleName ,globals(), locals(), [''])        
      clazz=getattr(mod,className)
        
      clazzInstance=clazz()
      return clazzInstance
    except:
      # sys.exc_info()[0] could be wrong
      message = ""
      for info in sys.exc_info():
        message = message + str(info)
      raise ClassLoaderException(message)
    
  def findByPattern(self, pattern):
    patternList = pattern.split(".")
    listLength=len(patternList)
    className=patternList[listLength-1]
    moduleName=".".join(patternList[0:listLength-1])
    return self.find(moduleName, className)

    
   
        
