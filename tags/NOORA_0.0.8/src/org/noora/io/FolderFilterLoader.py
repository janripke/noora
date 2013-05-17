#!/usr/bin/env python
from org.noora.io.Loadable import Loadable 
from org.noora.io.File import File
from org.noora.io.FileFolderFilter import FileFolderFilter

class FolderFilterLoader(Loadable):
  def __init__(self, filters):
    Loadable.__init__(self)
    self.__filters = filters

  def getFilters(self):
    return self.__filters
    
    
  def load(self, list = None):
    filters = self.getFilters()    
    
    for item  in list:
      file = File(item)
      filter = FileFolderFilter(file)
      filters.add(filter)

    return filters
  

       


