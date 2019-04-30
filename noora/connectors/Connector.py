from noora.connectors.Connectable import Connectable


class Connector(Connectable):
    """
    Connector base class. All technology connectors should inherit this.
    """
    def __init__(self):
        self.__result = None

    def get_result(self):
        return self.__result

    def set_result(self, result):
        self.__result = result

    def execute(self, executable, properties):
        """Override this method in a subclass"""
        raise NotImplementedError("execute method not implemented")
