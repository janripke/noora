#!/usr/bin/env python
from org.noora.io.Writeable import Writeable

class FileWriter(Writeable):
  def __init__(self, file=None):
    Writeable.__init__(self)
    self.__file = file
    pathName = file.getPath() + file.getName()            
    self.__handle = open(pathName,'wb')

  def getFile(self):
    return self.__file
    
  def fileno(self):
    handle = self.__handle
    return handle.fileno()    
    
  def write(self, buffer):
    handle = self.__handle
    handle.write(buffer)
    
  def close(self):
    handle = self.__handle
    handle.close()
    
    

       


