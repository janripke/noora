
class Outputable(object):
  """ Through this interface the output channel of a plugin is defined.
    The output channel may be the console, a database, the filesystem, etc...
    The channel is initialized, invoked and terminated through this interface.
  """

  def __init__(self):
    pass
  
  def initialize(self):
    pass
  
  def terminate(self):
    pass
  
  def processOutput(self):
    pass
