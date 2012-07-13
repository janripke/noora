#!/usr/bin/env python
import StreamHelper as StreamHelper
import NooraException as NooraException
M_LF = chr(10)

class ConfigReader:
    
  def __init__(self, filename):    
    self.__lines=[]
    self.__message=None
    self.loadFromFile(filename)
   
  def parse(self, stream):
    stream = StreamHelper.StreamHelper().convert(stream)
    lines = stream.split(chr(10))
    for line in lines:
      self.__lines.append(line)
    
  def loadFromFile(self, filename):
    try:
      handle=open(filename,'r')
      stream=handle.read()
      handle.close()
      self.parse(stream)
    except IOError:
      self.setMessage('project configuration file "' + filename + '" not found.')

  def saveToFile(self, filename):
    stream=M_LF.join(self.__lines)
    handle=open(filename,'w')
    handle.write(stream)
    handle.close()
      
  def getValue(self,keyword):
    lines=self.__lines
    for line in lines:
      if line.startswith(keyword):
        values=line.split('=')[1::]
        value='='.join(values)
        return eval(value)
    return None

  def setValue(self,keyword,value):
    lines=self.__lines
    for line in lines:
      if line.startswith(keyword):
        newLine=keyword+'='+str(value)
        lines[lines.index(line)] = newLine


  def hasValue(self, keyword, value):
    values=self.getValue(keyword)
    for val in values:
      if val.lower()==value.lower():
        return True
    return False

  def failOnValueNotFound(self, keyword, values, message):
    for value in values:
      if self.hasValue(keyword, value)==False:
        raise NooraException.NooraException(message)

  def failOnValueFound(self, keyword, values, message):
    for value in values:
      if self.hasValue(keyword, value)==True:
        raise NooraException.NooraException(message)

  def failOnConfigNotLoaded(self):
    if self.getMessage()!=None:
      print self.getMessage()
      exit(1)
        

  def setMessage(self, message):
    self.__message=message

  def getMessage(self):
    return self.__message





