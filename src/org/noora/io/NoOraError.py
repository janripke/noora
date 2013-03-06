

class NoOraError(Exception):

  def __init__(self, key, value):
    Exception.__init__(self)
    self.__errors = dict()
    self.__errors[key] = value
    
  def addReason(self, key, value):
    self.__errors[key] = value;
    return self
    
  def getReasons(self):
    return self.__errors;
        