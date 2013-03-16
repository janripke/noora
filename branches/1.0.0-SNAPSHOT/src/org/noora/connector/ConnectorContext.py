#!/usr/bin/env python

__revision__ = "$Revision: $"

class ConnectorContext:

    def __init__(self, params=None, options=None):
        self.params = params if params is not None else {}
        self.options = options if options is not None else []

    def isValid(self):
        if not "hostname" in self.params:
            return False
        if not "user" in self.params:
            return False;
        if not "password" in self.params:
            return False;
        else:
            return True;

    def paramNames(self):
        return [ "hostname", "user", "password" ];
