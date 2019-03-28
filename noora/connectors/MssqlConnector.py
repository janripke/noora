from noora.io.File import File
from noora.shell.Shell import Shell
from noora.shell.CallFactory import CallFactory

from noora.processor.PreProcessor import PreProcessor
from noora.connectors.Connector import Connector


class MssqlConnector(Connector):
    def execute(self, executable, properties):
        script = executable['script']

        cp = dict()
        cp['database'] = executable['database']
        if 'schema' in executable.keys():
            cp['schema'] = executable['schema']
        if 'environment' in properties.keys():
            cp['environment'] = properties.get('environment')
        if 'previous' in properties.keys():
            cp['previous'] = properties.get('previous')

        stream = PreProcessor.parse(script, cp)

        tmp = File("tmp.sql")
        f = open(tmp.get_url(), 'w')
        f.write(stream)
        f.close()

        # FIXME: remove?
        #script_reader = open(tmp.get_url())

        feedback = File('feedback.log')
        feedback_writer = open(feedback.get_url(), 'w')
        # FIXME: rewrite with format
        statement = "sqlcmd -b -S {host},{port} -U {user} -P {passwd} -d {db} -i {url}".format(
            host=executable['host'],
            port=executable.get('port') or 1433,
            user=executable['username'],
            passwd=executable['password'],
            db=executable['database'],
            url=tmp.get_url(),
        )

        call = CallFactory.new_call(statement)
        call['stdout'] = feedback_writer
        call['stderr'] = feedback_writer
        result = Shell.execute(call)
        self.set_result(result)

