from datetime import datetime


# Python 2-3 compatibility: xrange has been renamed to range in Python 3
# TODO: xrange below is used in methods that are not referenced in the project
try:
    xrange
except NameError:
    xrange = range


class Ora(object):
    def __init__(self):
        pass

    @staticmethod
    def nvl(*args):
        """
        Return the first argument, or the second argument if the first was not provided. Serves
        as default value selector.
        """
        count = len(args)
        if count != 2:
            raise ValueError("invalid number of arguments")

        if args[0]:
            return args[0]
        return args[1]

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def nvl2(*args):
        count = len(args)
        if count != 3:
            raise ValueError("invalid number of arguments")

        if args[0]:
            return args[1]
        return args[2]

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def nnvl(*args):
        count = len(args)
        if count != 2:
            raise ValueError("invalid number of arguments")

        if not args[0]:
            return args[0]
        return args[1]

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def nnvl2(*args):
        count = len(args)
        if count != 3:
            raise ValueError("invalid number of arguments")

        if not args[0]:
            return args[1]
        return args[2]

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def decode(*args):
        count = len(args)
        if count < 3:
            raise ValueError("not enough arguments for method")
        key = args[0]
        for i in xrange(1, count - 1, 2):
            if key == args[i]:
                return args[i+1]
        if count % 2 == 0:
            return args[count-1]

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def nnvl_decode(*args):
        count = len(args)
        if count < 3:
            raise ValueError("not enough arguments for method")
        for i in xrange(0, count - 1, 2):
            if args[i]:
                return args[i+1]
        if not count % 2 == 0:
            return args[count-1]

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def substr(s, start, count):
        if s:
            return s[start:count]
        return s

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def fsdate(s, string_format, target_format):
        if s:
            return datetime.strftime(datetime.strptime(s, string_format).date(), target_format)
        return None

    # TODO: this method is not used in the project. Maybe remove?
    @staticmethod
    def iif(*args):
        count = len(args)
        if count < 3:
            raise ValueError("not enough arguments for method")
        if args[1] in args[0]:
            return args[0][args[1]]
        return args[2]
