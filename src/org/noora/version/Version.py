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
  
  def getWeight(self):
    return self.__weight  
  
  def __eq__(self, other):
    if self.getValue() == other.getValue():  # compare name value (should be unique)
      return 1
    else: return 0  