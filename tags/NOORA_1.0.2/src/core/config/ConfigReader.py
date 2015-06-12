
CR_STATUS_NOT_LOADED = 1
CR_STATUS_LOADED = 2
CR_STATUS_ERROR = 3

class ConfigReader:


    def __init__(self, filename):
        self.__filename = filename
        self.__status = CR_STATUS_NOT_LOADED
        self.__message = None

    def load(self):
        self.__message = "Unsupported operation: load"

    def save(self):
        self.__message = "Unsupported operation: save"

    def getValue(self, path):
        self.__message = "Unsupported operation: getValue"

    def setValue(self, path, value):
        self.__message = "Unsupported operation: setValue"

    def hasValue(self, path):
        self.__message = "Unsupported operation: hasValue"

    def setFilename(self, filename):
        self.__filename = filename
        self.__status = CR_STATUS_NOT_LOADED
        self.__message = None

    def getFilename(self):
        return self.__filename

    def setStatus(self, status):
        self.__status = status

    def getStatus(self):
        return self.__status

    def setMessage(self, message):
        self.__message = message

    def getMessage(self):
        return self.__message
