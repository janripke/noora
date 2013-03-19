
from org.noora.io.NoOraError import NoOraError

class Configurable:

#---------------------------------------------------------
  def __init__(self):
    pass

#---------------------------------------------------------
  def load(self):
    raise NoOraError('detail', "message not implemented")

#---------------------------------------------------------
  def getProperty(self, name):
    raise NoOraError('detail', "message not implemented")

#---------------------------------------------------------
  def setProperty(self, name, value):
    raise NoOraError('detail', "message not implemented")
  
#---------------------------------------------------------
  def getElement(self, name):
    raise NoOraError('detail', "message not implemented")

