from org.noora.io.NoOraError import NoOraError

class Inputable(object):
    
  def __init__(self):
    pass
        
  def initialize(self):
    pass
  
  def terminate(self):
    pass
  
  def fetchInput(self, what):
    raise NoOraError('detail', "method not implemented")
  