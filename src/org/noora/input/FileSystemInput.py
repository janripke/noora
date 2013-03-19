from org.noora.input.Inputable import Inputable
from org.noora.output.Outputable import Outputable

class FileSystemInput(Inputable):

  def __init__(self):
    Inputable.__init__(self)
  
  def initialize(self):
    pass
  
  def terminate(self):
    pass
  
  def fetchInput(self, what):
    return ""
