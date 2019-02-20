#!/usr/bin/env python

class MissingOptionException(Exception):
    
  def __init__(self, message, missingOptions):
    Exception.__init__(self)
            
    self.__missingOptions=missingOptions
    for missingOption in missingOptions:
      message = message + " " + missingOption.getType() + ","
      message = message.rstrip(',')
    self.__message=message  

  def __str__(self):
    return repr(self.__message)

  def getMessage(self):
    return self.__message
  
  def getMissingOptions(self):
    return self.__missingOptions
