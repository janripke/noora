#!/usr/bin/env python

class InvalidEnvironmentException(Exception):
    
  def __init__(self, message, environment):
    Exception.__init__(self)            
    self.__environment=environment    
    message = message + " " + environment 
    self.__message=message  

  def __str__(self):
    return repr(self.__message)

  def getMessage(self):
    return self.__message
  
  def getInvalidEnvironment(self):
    return self.__environment
