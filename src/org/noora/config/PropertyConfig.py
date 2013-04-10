
from org.noora.config.Configurable import Configurable
from org.noora.io.PropertyFileReader import PropertyFileReader
from org.noora.io.NoOraError import NoOraError

import re

class PropertyConfig(Configurable):
  
#---------------------------------------------------------
  def __init__(self, _file):
    Configurable.__init__(self)
    
    self.__reader = PropertyFileReader(_file)
    self.__values = {}

#---------------------------------------------------------
  def load(self):
    self.__reader.read()
    
    regex = re.compile(r"^\s*(\w+)\s*=\s*(.+)$")
    empty = re.compile(r"^\s*$")
    comment = re.compile(r"^\s*#")
    
    lines = self.__reader.getLines()
    for line in lines:
      
      isEmpty = empty.match(line)
      if isEmpty:
        continue
      isComment = comment.match(line)
      if isComment:
        continue
      
      m = regex.match(line)
      groups = m.groups()
      if len(groups) == 2:
        self.__values[m.group(1)] = eval(m.group(2))
 
#---------------------------------------------------------
  def getProperty(self, name):
    return self.__values[name]

#---------------------------------------------------------
  def setProperty(self, name, value):
    raise NoOraError('detail', "method not implemented")
  
        