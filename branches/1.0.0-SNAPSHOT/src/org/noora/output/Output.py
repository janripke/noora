from org.noora.output.Outputable import Outputable

class Output(Outputable):
  
  def __init__(self, plugin = None):
    self.__plugin = plugin
  
#---------------------------------------------------------
  def write(self, where, what, content):
    if self.__plugin:
      generator = self.__plugin.getGenerator()
      if generator:
        content = generator.replaceGeneratedValues(content)
        
    self.outputContent(where, what, content)

#---------------------------------------------------------
# accessors
#---------------------------------------------------------
  def getPlugin(self):
    return self.__plugin
  
#---------------------------------------------------------
  def setPlugin(self,plugin):
    self.__plugin = plugin