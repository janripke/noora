from org.noora.output.Outputable import Outputable
from wheezy.template.engine import Engine
from wheezy.template.loader import DictLoader
from wheezy.template.ext.core import CoreExtension


class Output(Outputable):
  
  def __init__(self, plugin = None):
    self.__plugin = plugin
  
#---------------------------------------------------------
  def write(self, where, what, content):
    if self.__plugin:
      
      # apply template substitution to content
      content = self.__applyTemplateSubstitution(content);
       
    self.outputContent(where, what, content)

#---------------------------------------------------------
# accessors
#---------------------------------------------------------
  def getPlugin(self):
    return self.__plugin
  
#---------------------------------------------------------
  def setPlugin(self,plugin):
    self.__plugin = plugin
    
#---------------------------------------------------------
# private methods
#---------------------------------------------------------
  def __applyTemplateSubstitution(self, content):
    generator = self.__plugin.getGenerator()
    if generator:
      
      engine = Engine(loader     = DictLoader({ 'template' : content}),
                      extensions = [ CoreExtension() ])
      template = engine.get_template('template')
      content = template.render({ 'generator' : generator })
      
    return content

    