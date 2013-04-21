from org.noora.input.Inputable import Inputable
from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.io.NoOraError import NoOraError
import os


class FileSystemInput(Inputable):

  def __init__(self):
    Inputable.__init__(self)
  
  def initialize(self):
    pass
  
  def terminate(self):
    pass
  
  def fetchInput(self, where, what):
    
    if not what:
      raise NoOraError('detail', "invalid parameter value").addReason('parameter', 'what')
    if not where:
      where = "."
    
    inputFile = File(os.sep.join( [ where, what ] ))
    if not inputFile.exists():
      raise NoOraError('detail', 'file does not exist').addReason('filename', what).addReason('where', where)
    
    try:
      reader = FileReader(inputFile)
      content = reader.read()
      reader.close()
      return content
    except Exception as e:
      ex =  NoOraError('detail', "cannot read file")
      ex.addReason('filename', what)
      ex.addReason('reason', e)
      raise ex
