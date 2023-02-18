from noora.exceptions.io_exception import IOException


class Filterable(object):
    def accept(self, fileable):
        raise IOException("method not implemented")
