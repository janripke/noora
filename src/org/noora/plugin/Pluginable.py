
from org.noora.io.NoOraError import NoOraError

class Pluginable:
  
#---------------------------------------------------------
  def __init__(self, name, application, inputObject, outputObject):
    pass

#---------------------------------------------------------
  def initialize(self):
    raise NoOraError('detail', "method not implemented")
  
#---------------------------------------------------------
  def terminate(self):
    raise NoOraError('detail', "method not implemented")

#---------------------------------------------------------
  def execute(self):
    raise NoOraError('detail', "method not implemented")
  
#---------------------------------------------------------
  def getName(self):
    raise NoOraError('detail', "method not implemented")
