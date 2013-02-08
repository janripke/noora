#!/usr/bin/env python

class ConnectorContext:

    def __init__(self, params = None, args = None):
        self.params = params if params is not None else {}
        self.args = args if args is not None else []
        
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
