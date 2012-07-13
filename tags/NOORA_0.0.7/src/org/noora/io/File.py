#!/usr/bin/env python
from org.noora.io.Fileable import Fileable
import os

class File(Fileable):
  def __init__(self, pathName=None):
    Fileable.__init__(self)
    self.__pathName=pathName
    
  @staticmethod
  def pathSeperator():
    return os.sep    
    
  def exists(self):
    if self.isFile():
      return True
    if self.isDirectory():
      return True
    return False
      
  def notExists(self):
    if self.exists():
      return False
    return True
  
  def isFile(self):
    pathName = self.__pathName
    return os.path.isfile(pathName)
  
  def isDirectory(self):
    pathName = self.__pathName
    return os.path.isdir(pathName)
  
  def getName(self):
    pathName = self.__pathName
    folder,filename=os.path.split(pathName)
    return filename
  
  def getPath(self):
    pathName = self.__pathName
    folder,filename=os.path.split(pathName)
    return folder

  def getExtension(self):
    pathName = self.__pathName
    root,extension=os.path.splitext(pathName)
    return extension.lstrip('.')  
  
  def getRoot(self):
    pathName = self.__pathName
    root,extension=os.path.splitext(pathName)
    return root 

  def delete(self):
    pathName = self.__pathName
    if self.isFile():      
      os.remove(pathName)
    if self.isDirectory():
      os.rmdir(pathName)

       


