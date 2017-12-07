class InvalidEnvironmentException(Exception):
    def __init__(self, message, environment):
        Exception.__init__(self)
        self.__message = message + " " + environment

    def __str__(self):
        return repr(self.__message)
