#!/usr/bin/env python
from org.noora.cl.Parseable import Parseable
from org.noora.cl.CommandLine import CommandLine


class PosixParser(Parseable):
  def __init__(self):
    Parseable.__init__(self)
    
  def parse(self, options=None, arguments=None): 
    commandLine = CommandLine()
    for argument in arguments:      
      values = argument.split('=')
      if options.hasOption(values[0])==True:
        option = options.getOption(values[0])          
        option.setValues(values[1:])
        commandLine.addOption(option)
        
    return commandLine