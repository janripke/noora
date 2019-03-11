class Plugin(object):
    """
    This is the base class to be used by all plugins.
    """
    # The DB connector class. Override on subclass.
    _connector = None

    def __init__(self, properties, connector):
        self._properties = properties
        self._connector = connector()
        self._arguments = {}

    def set_argument(self, arg, val):
        self._arguments[arg] = val

    def get_argument(self, arg):
        return self._arguments[arg]

    def get_connector(self):
        return self._connector()

    def prepare(self, *args):
        """
        The prepare method. This should be implemented by subclasses.
        """
        raise NotImplementedError("Plugin.prepare should be defined by subclasses")

    def execute(self, *args):
        """
        The execute method. This should be implemented by subclasses.
        """
        raise NotImplementedError("Plugin.execute should be defined by subclasses")
