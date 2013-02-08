#!/usr/bin/env python
from org.noora.io.IOException import IOException
from org.noora.io.File import File

class FileProvider:
  
  def __init__(self):
    pass
  
  def getFile(self):
    raise IOException("method not implemented")
  

class FileFormat(FileProvider):
  
  def __init__(self, property=None):
    self.__property = property
  
  def getFile(self):
    return File(self.__property.getValue())

class Adaptable:
  def __init__(self):
    pass
  
  def adapt(self):
    raise IOException("method not implemented")
  
class FileFormatAdapter(Adaptable):
  def adapt(self, property=None):
    return FileFormat(property)
          


