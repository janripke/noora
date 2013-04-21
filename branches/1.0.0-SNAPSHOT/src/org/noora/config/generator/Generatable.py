from org.noora.io.NoOraError import NoOraError

class Generatable(object):

  def __init__(self):
    pass
  
  def getGeneratedValue(self, name):
    NoOraError('detail', 'Method not implemented')
