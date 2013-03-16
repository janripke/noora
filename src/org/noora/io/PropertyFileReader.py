
from org.noora.io.FileReader import FileReader
from org.noora.io.NoOraError import NoOraError
from org.noora.io.Readable import Readable

class PropertyFileReader(Readable):

#---------------------------------------------------------
  def __init__(self, file):
    if file == None:
      raise NoOraError("parameter", "file")
    
    Readable.__init__(self)
    self.__file = file
    self.__lines = [];
    
#---------------------------------------------------------
  def read(self):
    reader = FileReader(self.__file)
    stream = reader.read();
    self.__lines = stream.split(chr(10))
    reader.close()
    
#---------------------------------------------------------
  def getLines(self):
    return self.__lines
   
#---------------------------------------------------------
  def close(self):
    pass