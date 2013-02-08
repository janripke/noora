#!/usr/bin/env python
from org.noora.io.Filterable import Filterable

class FileFilter(Filterable):

  def __init__(self, file):
    Filterable.__init__(self)
    self.__file = file
    
  def getFile(self):
    return self.__file
    
  def accept(self, fileable):
    file = self.getFile()
    #if fileable.isFile() and fileable.getName()==file.getName() :
    if fileable.getName()==file.getName() :      
      return True
    return False
       


