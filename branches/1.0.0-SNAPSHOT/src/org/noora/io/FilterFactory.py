#!/usr/bin/env python
from org.noora.cl.Option import Option
from org.noora.io.FileFolderFilter import FileFolderFilter
from org.noora.io.FileFilter import FileFilter
from org.noora.io.FileExtensionFilter import FileExtensionFilter


class FilterSelector:

  def __init__(self):
    pass
  
  @staticmethod
  def select(file = None):
    return FileFolderFilter(file) 
  
  

class FilterFactory:
  def __init__(self):
    pass
  
  @staticmethod
  def newFileFolderFilter(file = None):
    return FileFolderFilter(file) 

  @staticmethod
  def newFileExtensionFilter(file = None):
    return FileExtensionFilter(file) 
  
  @staticmethod
  def newFileFilter(file = None):
    return FileFilter(file) 
