class MissingArgumentException(Exception):
  def __init__(self, message, missingArguments):
    Exception.__init__(self)
            
    self.__missingArguments=missingArguments
    for missingArgument in missingArguments:
      message = message + " " + missingArgument.getType() + ","
      message = message.rstrip(',')
    self.__message=message  

  def __str__(self):
    return repr(self.__message)

  def getMessage(self):
    return self.__message
  
  def getMissingArguments(self):
    return self.__missingOptions
