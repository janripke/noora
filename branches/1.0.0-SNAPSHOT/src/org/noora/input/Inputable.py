from org.noora.io.NoOraError import NoOraError

class Inputable(object):
    
  def __init__(self):
    pass
        
  def initialize(self):
    pass
  
  def terminate(self):
    pass
  
  def fetchInput(self, where, what):
    raise NoOraError('detail', "method not implemented")
  
  def iterator(self):
    raise NoOraError('detail', "method not implemented")

#=========================================================

class InputIterable(object):
  
  def __init__(self, recursive):
    pass
  
  def hasNext(self):
    pass
  
  def getNext(self):
    pass