from org.noora.connector.Executable import Executable

__revision__ = "$Revision: $"


class Execute(Executable):
  def __init__(self):
    Executable.__init__(self)
    self.__ignoreErrors=False
    self.__script=None
        
  def setIgnoreErrors(self, ignoreErrors):
    self.__ignoreErrors=ignoreErrors

  def getIgnoreErrors(self):
    return self.__ignoreErrors
    
  def setScript(self, script):
    self.__script=script
    
  def getScript(self):
    return self.__script
    
    

