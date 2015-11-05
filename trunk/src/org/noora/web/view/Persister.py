import web

class Persister:

    def __init__(self):      
      self.__database = web.database(dbn='mysql', host='localhost', user='apps', pw='apps', db='orcl')      

    def getDatabase(self):
      return self.__database
    
