from noora.exceptions.IOException import IOException


class Filterable(object):
    def accept(self, fileable):
        raise IOException("method not implemented")
