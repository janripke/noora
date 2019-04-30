import subprocess

from noora.exceptions.plugins.PluginException import PluginException


class Shell(object):
    """Shell interaction"""
    @staticmethod
    def execute(call):
        """
        Execute the command in ``call``. Returns the standard output if
        execution was successful, raises an exception with results from
        standard error otherwise.

        :param call: A dictionary, containing:

            * **args**: The command to execute as a string;
            * **stdout**: File-like object to write standard output to (optional);
            * **stderr**: File-like object to write standard error to (optional);
            * **stdin**: File-like object to read standard input from (optional);
            * **startupinfo**: Extra flags (optional).

        :return: The result from standard output.
        """
        args = call['args']
        shell = call['shell']
        stdout = call['stdout']
        stderr = call['stderr']
        stdin = call['stdin']
        startupinfo = call['startupinfo']

        # TODO: Popen isn't used any more. Remove?
        #p = subprocess.Popen(args, shell=shell, stdin=stdin, stderr=stderr, startupinfo=startupinfo)

        result = subprocess.call(
            args, shell=True, stdin=stdin, stdout=stdout, stderr=stderr, startupinfo=startupinfo)

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
