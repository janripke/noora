from org.noora.io.Directory import Directory
from org.noora.io.File import File
from org.noora.io.FileWriter import FileWriter
from org.noora.io.NoOraError import NoOraError
from org.noora.output.Output import Output
import os

class FileSystemOutput(Output):

  def __init__(self, plugin = None):
    Output.__init__(self, plugin)
  
  def initialize(self):
    pass
  
  def terminate(self):
    pass
  
  def outputContent(self, where, what, content):
    
    if not what:
      raise NoOraError('detail', "invalid parameter value").addReason('parameter', 'what')
    if not where:
      where = "."
      
    if not File(where).exists():
      os.makedirs(where)
      
    workdir = Directory()
    workdir.pushDir(where)
    
    outputFile = File(what)
    if outputFile.exists():
      raise NoOraError('detail', 'file already exist').addReason('filename', what)
    
    try:
      writer = FileWriter(outputFile)
      writer.write(content)
      writer.close()
    except Exception as e:
      ex =  NoOraError('detail', "cannot write file")
      ex.addReason('filename', what)
      ex.addReason('reason', e)
      raise ex
    finally:
      workdir.popDir()
