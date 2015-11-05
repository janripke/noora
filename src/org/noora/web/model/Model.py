class Model:
  def __init__(self, db=None):
    self.__db=db
  
  def getDatabase(self):
    return self.__db
    
  def setDatabase(self, db):
    self.__db = db
