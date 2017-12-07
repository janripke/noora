#!/usr/bin/env python

class ClassLoader:
    def __init__(self):
        pass

    @staticmethod
    def find(pattern):
        pattern_list = pattern.split(".")
        count = len(pattern_list)
        class_name = pattern_list[count - 1]
        module_name = ".".join(pattern_list[0:count - 1])

        mod = __import__(module_name, globals(), locals(), [''])
        clazz = getattr(mod, class_name)
        instance = clazz()
        return instance
