
from org.noora.config.Configurable import Configurable
from org.noora.io.NoOraError import NoOraError
from org.noora.io.XmlFileReader import XmlFileReader

class XmlConfig(Configurable):
  
#---------------------------------------------------------
  def __init__(self, _file):
    Configurable.__init__(self)
    
    if _file == None:
      raise NoOraError('detail', "invalid argument 'file' (None)")
    self.__reader = XmlFileReader(_file)

#---------------------------------------------------------
  def load(self):
    self.__reader.read()

#---------------------------------------------------------
  def getProperty(self, name):
    """ note that name actually is an xpath expression """
    root = self.__reader.getHandle()
    elements = root.findall(name)
    
    if (elements):
      # assume that the first element contains the data we're interested in
      return elements[0].text
    else:
      return None

#---------------------------------------------------------
  def setProperty(self, name, value):
    raise NoOraError('detail', "method not implemented")

#---------------------------------------------------------
  def getElement(self, name):
    """ note that name actually is an xpath expression """
    root = self.__reader.getHandle()
    elements = root.findall(name)
    
    return elements
