class Filters(object):
    def __init__(self):
        self.__filters = []

    def add(self, filterable):
        self.__filters.append(filterable)

    def list(self):
        return self.__filters

    def accept(self, fileable):
        filters = self.__filters
        for filter in filters:
            if filter.accept(fileable):
                return True
        return False
