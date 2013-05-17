#!/usr/bin/env python
from org.noora.io.Loadable import Loadable 
from org.noora.io.File import File
from org.noora.io.FileExtensionFilter import FileExtensionFilter

class ExtensionFilterLoader(Loadable):
  def __init__(self, filters):
    Loadable.__init__(self)
    self.__filters = filters

  def getFilters(self):
    return self.__filters
    
    
  def load(self, list = None, filterType):
    filters = self.getFilters()    
    
    for item  in list:
      file = File(item)
      filter = FileExtensionFilter(file)
      filters.add(filter)

    return filters
  

       


