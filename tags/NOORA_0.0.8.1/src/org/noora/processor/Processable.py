#!/usr/bin/env python
from org.noora.processor.ProcessorException import ProcessorException

class Processable:
  
  def __init__(self):
    pass
 
  def call(self, callable):
    raise ProcessorException("method not implemented") 
  




