from noora.io.IOException import IOException


class Filterable(object):
    def accept(self, fileable):
        raise IOException("method not implemented")
