#!/usr/bin/env python


class Plugin:
    def __init__(self, type, connectable):
        self.__type = type
        self.__connectable = connectable
        self.__executable = None

    def set_connector(self, connectable):
        self.__connectable = connectable

    def get_connector(self):
        return self.__connectable

    def set_executor(self, executable):
        self.__executable = executable

    def get_executor(self):
        return self.__executable

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type
