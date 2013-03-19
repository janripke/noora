#!/usr/bin/env python
from org.noora.classloader.ClassLoadable import ClassLoadable
from org.noora.io.NoOraError import NoOraError

import sys


class ClassLoader(ClassLoadable):
    
  def __init__(self):
    ClassLoadable.__init__(self)
    
  def importClass(self, moduleName, className):
    try:
      mod = __import__(moduleName ,globals(), locals(), [''])        
      clazz=getattr(mod,className)      
      return clazz
    except:
      # sys.exc_info()[0] could be wrong
      message = ""
      for info in sys.exc_info():
        message = message + str(info)
      e = NoOraError('detail', "cannot load class {0}.{1}".format(moduleName, className))
      e.addReason('class', moduleName + "." + className)
      e.addReason('exc_info', message)
      raise e
    
  def find(self, moduleName, className, args):
    l = 0
    
    clazz = self.importClass(moduleName, className)
    if args:
      l = len(args)
    
    if l == 0:
      return clazz()
    elif l == 1:
      return clazz(args[0])
    elif l == 2:
      return clazz(args[0], args[1])
    elif l == 3:
      return clazz(args[0], args[1], args[2])
    elif l == 4:
      return clazz(args[0], args[1], args[2], args[3])
    else:
      raise NoOraError('detail', "number of args for classloader is too large to handle (>4)")
     
  def findByPattern(self, pattern, args):
    patternList = pattern.split(".")
    listLength=len(patternList)
    className=patternList[listLength-1]
    moduleName=".".join(patternList[0:listLength-1])
    return self.find(moduleName, className, args)

    
   
        
