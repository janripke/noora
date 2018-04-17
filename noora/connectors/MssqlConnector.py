from noora.connectors.Connector import Connector
from noora.system.Properties import Properties
from noora.processor.PreProcessor import PreProcessor
from noora.io.File import File
from noora.shell.Shell import Shell
from noora.shell.CallFactory import CallFactory


class MssqlConnector(Connector):
    def __init__(self):
        Connector.__init__(self)
        self.__result = None

    def get_result(self):
        return self.__result

    def set_result(self, result):
        self.__result = result

    def execute(self, executable, properties):
        script = executable['script']

        cp = Properties()
        cp.set_property('database', executable['database'])
        if 'schema' in executable.keys():
            cp.set_property('schema', executable['schema'])
        if 'environment' in properties.keys():
            cp.set_property('environment', properties.get_property('environment'))
        if 'previous' in properties.keys():
            cp.set_property('previous', properties.get_property('previous'))

        stream = PreProcessor.parse(script, cp)

        tmp = File("tmp.sql")
        f = open(tmp.get_url(), 'w')
        f.write(stream)
        f.close()

        #script_reader = open(tmp.get_url())

        feedback = File('feedback.log')
        feedback_writer = open(feedback.get_url(), 'w')
        statement = "sqlcmd -b -S " + executable['host'] + " -U " + executable['username'] + ' -P ' + executable['password'] + " -d " + executable['database'] + " -i " + tmp.get_url()

        call = CallFactory.new_call(statement)
        call['stdout'] = feedback_writer
        call['stderr'] = feedback_writer
        result = Shell.execute(call)
        self.set_result(result)

