import subprocess
from noora.plugins.PluginException import PluginException


class Shell:
    def __init__(self):
        pass

    @staticmethod
    def execute(call):
        args = call['args']
        shell = call['shell']
        stdout = call['stdout']
        stderr = call['stderr']
        stdin = call['stdin']
        startupinfo = call['startupinfo']

        #p = subprocess.Popen(args, shell=shell, stdin=stdin, stderr=stderr, startupinfo=startupinfo)
        result = subprocess.call(args, shell=True, stdin=stdin, stdout=stdout, stderr=stderr, startupinfo=startupinfo)
        #output = p.communicate()
        #if p.returncode != 0:
        if result != 0:
            f = open(stderr.name)
            stream = f.read()
            f.close()
            raise PluginException(stream)

        f = open(stdout.name)
        stream = f.read()
        f.close()
        return stream
