class IOException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.__message = message

    def __str__(self):
        return repr(self.__message)
