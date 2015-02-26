import os

class Path:
  def __init__(self):
    pass
  
  @staticmethod
  def path(*args):
    result = ''
    for arg in args:
      if arg:
        result = result + arg + os.sep
    return result.rstrip(os.sep)