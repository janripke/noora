class Version:
    def __init__(self, value):
        self.__value = value

        i = 0
        result = 0
        for item in value.split('.'):
            result = result + int(item) * 1000 ^ i
            i = i + 1
        self.__weight = result

    def get_value(self):
        return self.__value

    def to_string(self):
        return self.__value

    def get_mayor(self):
        value = self.__value
        if len(value.split('.')) >= 1:
            return value.split('.')[0]

    def get_minor(self):
        value = self.__value
        if len(value.split('.')) >= 2:
            return value.split('.')[1]

    def get_revision(self):
        value = self.__value
        if len(value.split('.')) >= 3:
            return value.split('.')[2]

    def get_patch(self):
        value = self.__value
        if len(value.split('.')) >= 4:
            return value.split('.')[3]

    def has_mayor(self):
        if self.get_mayor():
            return True
        return False

    def has_minor(self):
        if self.get_minor():
            return True
        return False

    def has_revision(self):
        if self.get_revision():
            return True
        return False

    def has_patch(self):
        if self.get_patch():
            return True
        return False

    def get_weight(self):
        return self.__weight

    def __eq__(self, other):
        if self.get_value() == other.get_value():  # compare name value (should be unique)
            return 1
        else:
            return 0
