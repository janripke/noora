import sys

class NoOraError(Exception):

  def __init__(self, key, value):
    Exception.__init__(self)
    self.__errors = dict()
    self.__errors[key] = value
    
    frame = sys._getframe(1)
    self.__errors["func"] = frame.f_code.co_name
    self.__errors["file"] = frame.f_code.co_filename
    self.__errors["line"] = frame.f_lineno
    
  def addReason(self, key, value):
    self.__errors[key] = value;
    return self
    
  def getReasons(self):
    return self.__errors;
  
  def getMessage(self):
    if 'detail' in self.__errors:
      return self.__errors['detail']
    else:
      return type(self)
    
  def getUserReason(self):
    if 'usermsg' in self.__errors:
      return self.__errors['usermsg']
    return ""
  
  def getDiagnostics(self):
    diag = [];
    for key in self.__errors:
      diag.append("{0}={1}".format(key, self.__errors[key]))
    return ", ".join(diag)
        