
from org.noora.io.NoOraError import NoOraError

# return values for self.execute
PER_EXIT = 1
PER_CONTINUE = 2

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
    """ Perform the plugin's functionality
      @return returns PER_STOP when additional processing is not desired (e.g. after running the 'help' plugin
    """
    raise NoOraError('detail', "method not implemented")

#---------------------------------------------------------
  def getName(self):
    raise NoOraError('detail', "method not implemented")

#---------------------------------------------------------
  def getOptions(self):
    raise NoOraError('detail', "method not implemented")