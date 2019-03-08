class Plugin(object):
    """
    This is the base class to be used by all plugins.
    """
    # The DB connector class. Override on subclass.
    _connector = None
    # The default excecute method for this plugin
    _executable = 'execute'
    # If the command provides functionality outside of the project scope, set this variable
    _executable_outside_scope = None

    @classmethod
    def get_connector(cls):
        return cls._connector()

    @classmethod
    def get_executor(cls, outside_scope=False):
        if not outside_scope:
            return getattr(cls, cls._executable)
        if outside_scope:
            return getattr(cls, cls._executable_outside_scope)

    @staticmethod
    def execute(*args):
        """
        The execute method. This should be implemented by subclasses.
        """
        raise NotImplementedError("Plugin.execute should be defined by subclasses")
