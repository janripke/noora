class Properties:
    def __init__(self):
        self.__properties = {}

    def get_properties(self):
        return self.__properties

    def keys(self):
        properties = self.get_properties()
        return properties.keys()

    def set_property(self, key, value):
        properties = self.get_properties()
        properties[key] = value

    def get_property(self, key):
        properties = self.get_properties()
        return properties[key]
