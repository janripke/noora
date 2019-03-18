class Plugin(object):
    """
    This is the base class to be used by all plugins.
    """
    _connectable = None

    def __init__(self, connectable=None):
        """
        Initialize the class.

        :param connectable: If set, initializes the connectable and sets this
            as connector on the class instead of the default connectable class.
            This allows you to override a connector for a technology without
            having to define a new plugin class.
        """
        if connectable:
            self._connector = connectable()
        else:
            self._connector = self._connectable()

    def get_connector(self):
        return self._connector

    def _validate_and_prepare(self, properties, arguments):
        """
        Internal method called by execute to validate and prepare the arguments.

        :param properties: An initialized noora.system.Properties.Properties class
        :param arguments: A dict containing the arguments for execution
        """
        raise NotImplementedError("Plugin._validate_and_prepare should be defined by subclasses")

    def execute(self, properties, arguments):
        """
        The execute method. This should be implemented by subclasses.

        :param properties: An initialized noora.system.Properties.Properties class
        :param arguments: A dict containing the arguments for execution
        """
        raise NotImplementedError("Plugin.execute should be defined by subclasses")
