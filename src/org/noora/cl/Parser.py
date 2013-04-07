#!/usr/bin/env python
from org.noora.cl.Parseable import Parseable
from org.noora.cl.CommandLine import CommandLine
from org.noora.cl.MissingOptionException import MissingOptionException
from org.noora.cl.MissingArgumentException import MissingArgumentException
from org.noora.cl.UnrecognizedOptionException import UnrecognizedOptionException
from org.noora.cl.UnrecognizedArgumentException import UnrecognizedArgumentException

class Parser(Parseable):
  
  def __init__(self):
    Parseable.__init__(self)
    self.__options = None
    self.__commandLine = None
    
  def checkRequiredOptions(self):    
    options=self.__options
    commandLineList=self.__commandLine.getOptions().getOptions()    
    missingOptions = []
    
    for option in options.getRequiredOptions():
      if option not in commandLineList:
        missingOptions.append(option) 
      
    if missingOptions:   
      raise MissingOptionException('missing option',missingOptions)

  def checkUnrecognizedOptions(self):    
    options=self.__options
    commandLineList=self.__commandLine.getOptions().getOptions()    
    missingOptions = []
    
    for option in options.getRequiredOptions():
      if option not in commandLineList:
        missingOptions.append(option) 
      
    if missingOptions:   
      raise MissingOptionException('missing option',missingOptions)

    
  def checkRequiredArguments(self):
    
    missingArguments = self.__commandLine.getRequiredArguments()
    if missingArguments:
      raise MissingArgumentException('missing argument in option',missingArguments)
    
      
  def parse(self, options=None, arguments=None, stopAtNonRecognizedOption=False):
    self.__options = options
    self.__arguments = arguments
    self.__commandLine = CommandLine()
    for argument in arguments:      
      values = argument.split('=')
      if options.hasOption(values[0])==True:          
          option = options.getOption(values[0])  
          
          if option.hasValues():
            for argumentValue in values[1:]:
              if argumentValue not in option.getValues():
                raise UnrecognizedArgumentException("unrecognized argument",argumentValue)
        
          if values[1:]!=['']:        
            option.setValues(values[1:])
          self.__commandLine.addOption(option)
      else:
        if stopAtNonRecognizedOption:
          raise UnrecognizedOptionException('unrecognized option',values[0])
          
        
    return self.__commandLine