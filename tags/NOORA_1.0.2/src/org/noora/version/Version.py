class Version:
  
  def __init__(self, value):
    self.__value = value
    
    i = 0
    result = 0
    for item in value.split('.'):
      result = result + int(item) * 1000^i
      i = i + 1
    self.__weight = result
    
  def getValue(self):
    return self.__value
  
  def toString(self):
    return self.__value
  
  def getMayor(self):
    value = self.__value
    if len(value.split('.'))>= 1:
      return value.split('.')[0]
  
  def getMinor(self):
    value = self.__value
    if len(value.split('.'))>= 2:
      return value.split('.')[1]
  
  def getRevision(self):
    value = self.__value
    if len(value.split('.'))>= 3:
      return value.split('.')[2]
  
  def getPatch(self):
    value = self.__value
    if len(value.split('.'))>= 4:
      return value.split('.')[3]
    
  def hasMayor(self):
    if self.getMayor():
      return True
    return False
  
  def hasMinor(self):
    if self.getMinor():
      return True
    return False
  
  def hasRevision(self):
    if self.getRevision():
      return True
    return False
  
  def hasPatch(self):
    if self.getPatch():
      return True
    return False
      
    
  
  def getWeight(self):
    return self.__weight  
  
  def __eq__(self, other):
    if self.getValue() == other.getValue():  # compare name value (should be unique)
      return 1
    else: return 0  