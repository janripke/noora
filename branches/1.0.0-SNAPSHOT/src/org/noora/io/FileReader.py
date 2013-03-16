#!/usr/bin/env python
from org.noora.io.NoOraError import NoOraError
from org.noora.io.Readable import Readable
import os

class FileReader(Readable):
  
  def __init__(self, file=None):
    """
      Initializes and opens the specified File
      @param file File object
      @throws NoOraError('file', 'cannot open &lt;filename&gt;') 
    """
    Readable.__init__(self)
    self.__file = file
    if file.getPath()!='':
      pathName = file.getPath() + os.sep + file.getName()
    else:
      pathName = file.getPath() + file.getName()
      
    try:
      self.__handle = open(pathName,'rb')
    except IOError:
      raise NoOraError("file", "cannot open file {}".format(pathName))

  def fileno(self):
    handle = self.__handle
    return handle.fileno()    
    
  def read(self):
    """
      Reads the (already open) file. 
      Any CRLF or CR is translated to a single LF.
      @return a stream object
      @throws NoOraError("file", "cannot read file")
    """
    try:
      handle = self.__handle
      stream = handle.read()
      stream = stream.replace(chr(13)+chr(10),chr(10))
      stream = stream.replace(chr(13),chr(10)) 
    except IOError:
      raise NoOraError("file", "cannot read file")
    return stream
  
  def getFile(self):
    return self.__file
    
  def close(self):
    handle = self.__handle
    handle.close()
    

       


