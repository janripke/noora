# TODO: is it necessary to explicitly implement __str__? I don't think so.
class UnknownVersionException(Exception):
    def __init__(self, message, version):
        Exception.__init__(self)
        self.__message = message + " " + version

    def __str__(self):
        return repr(self.__message)
