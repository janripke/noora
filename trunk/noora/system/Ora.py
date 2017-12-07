from datetime import datetime


class Ora:
    def __init__(self):
        pass

    @staticmethod
    def nvl(*args):
        count = len(args)
        if count != 2:
            raise "invalid number of arguments"

        if args[0]:
            return args[0]
        return args[1]

    @staticmethod
    def nvl2(*args):
        count = len(args)
        if count != 3:
            raise "invalid number of arguments"

        if args[0]:
            return args[1]
        return args[2]

    @staticmethod
    def nnvl(*args):
        count = len(args)
        if count != 2:
            raise "invalid number of arguments"

        if not args[0]:
            return args[0]
        return args[1]

    @staticmethod
    def nnvl2(*args):
        count = len(args)
        if count != 3:
            raise "invalid number of arguments"

        if not args[0]:
            return args[1]
        return args[2]

    @staticmethod
    def decode(*args):
        count = len(args)
        if count < 3:
            raise "not enough arguments for method"
        key = args[0]
        for i in xrange(1, count - 1, 2):
            if key == args[i]:
                return args[i+1]
        if count % 2 == 0:
            return args[count-1]

    @staticmethod
    def nnvl_decode(*args):
        count = len(args)
        if count < 3:
            raise "not enough arguments for method"
        for i in xrange(0, count - 1, 2):
            if args[i]:
                return args[i+1]
        if not count % 2 == 0:
            return args[count-1]

    @staticmethod
    def substr(s, start, count):
        if s:
            return s[start:count]
        return s

    @staticmethod
    def fsdate(s, string_format, target_format):
        if s:
            return datetime.strftime(datetime.strptime(s, string_format).date(), target_format)
        return None

    @staticmethod
    def iif(*args):
        count = len(args)
        if count < 3:
            raise "not enough arguments for method"
        if args[0].has_key(args[1]):
            return args[0][args[1]]
        return args[2]
