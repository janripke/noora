from noora.shell.StartupInfoFactory import StartupInfoFactory


class CallFactory(object):
    @staticmethod
    def new_call(args):
        call = {
            'args': args,
            'shell': True,
            'stdin': None,
            'stderr': None,
            'startupinfo': StartupInfoFactory.new_startup_info(),
        }
        return call
