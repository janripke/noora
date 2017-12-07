from noora.shell.StartupInfoFactory import StartupInfoFactory


class CallFactory:
    def __init__(self):
        pass

    @staticmethod
    def new_call(args):
        call = {}
        call['args'] = args
        call['shell'] = True
        call['stdin'] = None
        call['stderr'] = None
        call['startupinfo'] = StartupInfoFactory.new_startup_info()
        return call
