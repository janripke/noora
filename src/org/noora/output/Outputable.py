
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
  
  def processOutput(self, what, content):
    """
      Process the given output to a medium that is defined by the specialized outputable implementation
      @param what The name of the content (for instance a filename in case of an sql-script)
      @param content the actual content to 'output'
    """
    pass
