#!/usr/bin/env python

class UnrecognizedArgumentException(Exception):
    
  def __init__(self, message, unrecognizedArgument):
    Exception.__init__(self)            
    self.__unrecognizedArgument=unrecognizedArgument    
    message = message + " " + unrecognizedArgument 
    self.__message=message  

  def __str__(self):
    return repr(self.__message)

  def getMessage(self):
    return self.__message
  
  def getUnrecognizedArgument(self):
    return self.__unrecognizedArgument
