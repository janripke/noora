from org.noora.output.Outputable import Outputable

class DatabaseOutput(Outputable):

  def __init__(self):
    Outputable.__init__(self)
    self.__connector = None
  
  def initialize(self):
    pass
  
  def terminate(self):
    pass
  
  def processOutput(self, what, content):
    print content
