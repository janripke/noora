class Version(object):
    """Inspection class for a version string."""
    def __init__(self, value):
        """
        Initialize the version by splitting its parts and calculating the weight.

        :param value: A version in the form of A[.B[.C[.D]]]
        """
        self.__value = value

        i = 0
        result = 0
        for item in value.split('.'):
            # FIXME: if you have more than 1000 versions of a version part,
            # this will give you bad times
            result = result + float(item) / 1000**i
            i = i + 1
        self.__weight = result

    def get_value(self):
        """Get version"""
        return self.__value

    def to_string(self):
        return self.__value

    def get_major(self):
        """Return major part of the version"""
        value = self.__value
        if len(value.split('.')) >= 1:
            return value.split('.')[0]

    def get_minor(self):
        """Return minor version part, if applicable"""
        value = self.__value
        if len(value.split('.')) >= 2:
            return value.split('.')[1]

    def get_revision(self):
        """Return revision part, if applicable"""
        value = self.__value
        if len(value.split('.')) >= 3:
            return value.split('.')[2]

    def get_patch(self):
        """Get patch version, if applicable"""
        value = self.__value
        if len(value.split('.')) >= 4:
            return value.split('.')[3]

    def has_major(self):
        """Return True if version has a major part"""
        if self.get_major():
            return True
        return False

    def has_minor(self):
        """Return True if version has a minor part"""
        if self.get_minor():
            return True
        return False

    def has_revision(self):
        """Return True if version has a revision part"""
        if self.get_revision():
            return True
        return False

    def has_patch(self):
        """Return True if version has a patch part"""
        if self.get_patch():
            return True
        return False

    def get_weight(self):
        """Return weight of the version"""
        return self.__weight

    def __eq__(self, other):
        """Compare two versions. Return 1 if the versions are the same, 0 otherwise"""
        if self.get_value() == other.get_value():  # compare name value (should be unique)
            return 1
        else:
            return 0
