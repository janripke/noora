# TODO: is it necessary to explicitly implement __str__? I don't think so
class BlockedHostException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.__message = message

    def __str__(self):
        return repr(self.__message)


