#!/usr/bin/env python
from org.noora.processor.Processable import Processable
from org.noora.processor.ProcessorException import ProcessorException
from org.noora.processor.ProcessorResult import ProcessorResult
from org.noora.io.FileReader import FileReader
import subprocess


class Processor(Processable):
  
  STDOUT          = "STDOUT"
  STDIN           = "STDIN"
  STDERR          = "STDERR"
  STARTUPINFO     = "STARTUPINFO"
  ARGUMENT        = "ARGUMENT"
  SHELL           = "SHELL"
  OK              = "OK"
  ERROR           = "ERROR"
  
  def __init__(self):
    Processable.__init__(self)
  
  def call(self, callable):
    try:
      shell = callable.getProperty(Processor.SHELL)
      stdout = callable.getProperty(Processor.STDOUT)
      stdin = callable.getProperty(Processor.STDIN)
      stderr = callable.getProperty(Processor.STDERR)
      startupinfo = callable.getProperty(Processor.STARTUPINFO)
      argument = callable.getProperty(Processor.ARGUMENT)
    
      result=subprocess.call(argument,shell=shell,stdout=stdout,stderr=stderr,stdin=stdin,startupinfo=startupinfo)
      if result!=0:
        file = stderr.getFile()
        reader = FileReader(file)
        stream = reader.read()     
        raise ProcessorException(stream)
      
      file = stdout.getFile()
      reader = FileReader(file)
      stream = reader.read()           
      return ProcessorResult(stream)
          
    except OSError:
      raise ProcessorException("Could not execute call. Is it installed and in your path?")

      
  
  




