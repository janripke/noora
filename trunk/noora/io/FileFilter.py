from noora.io.Filterable import Filterable


class FileFilter(Filterable):
    def __init__(self, file):
        Filterable.__init__(self)
        self.__file = file

    def get_file(self):
        return self.__file

    def accept(self, fileable):
        file = self.get_file()
        if fileable.tail() == file.tail():
            return True
        return False
