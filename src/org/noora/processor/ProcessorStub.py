#!/usr/bin/env python
from org.noora.processor.Processable import Processable
from org.noora.processor.ProcessorException import ProcessorException
from org.noora.io.FileReader import FileReader
import subprocess


class ProcessorStub(Processable):
  
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
      stderr = callable.getProperty(ProcessorStub.STDERR)
    
      result=0
      if result!=0:
        file = stderr.getFile()
        reader = FileReader(file)
        stream = reader.read()     
        raise ProcessorException(stream)    
    except OSError:
      raise ProcessorException("Could not execute call. Is it installed and in your path?")

      
  
  




