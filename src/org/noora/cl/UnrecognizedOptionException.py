class UnrecognizedOptionException(Exception):
  def __init__(self, message, unrecognizedOptions):
    Exception.__init__(self)
            
    self.__unrecognizedOptions=unrecognizedOptions
    for unrecognizedOption in unrecognizedOptions:
      message = message + " " + unrecognizedOption.getType() + ","
      message = message.rstrip(',')
    self.__message=message  

  def __str__(self):
    return repr(self.__message)

  def getMessage(self):
    return self.__message
  
  def getMissingOptions(self):
    return self.__unrecognizedOptions
