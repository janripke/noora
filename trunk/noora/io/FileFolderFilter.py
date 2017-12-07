from noora.io.Filterable import Filterable


class FileFolderFilter(Filterable):
    def __init__(self, file):
        Filterable.__init__(self)
        self.__file = file

    def get_file(self):
        return self.__file

    def accept(self, fileable):
        file = self.get_file()
        if fileable.is_dir() and fileable.tail() == file.tail():
            return True
        return False
