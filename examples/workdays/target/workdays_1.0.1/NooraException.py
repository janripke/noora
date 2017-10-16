class NooraException(Exception):
    
    def __init__(self, message):
        self.__message=message

    def __str__(self):
        return repr(self.__message)

    def getMessage(self):
        return self.__message
