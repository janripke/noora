from io import StringIO

from noora.io.File import File
from noora.shell.Shell import Shell
from noora.shell.CallFactory import CallFactory

from noora.processor.PreProcessor import PreProcessor
from noora.connectors.Connector import Connector


class PGSQLConnector(Connector):
    """
    Connector for PostGreSQL server.
    """
    def execute(self, executable, properties):
        """
        Execute the script provided by `executable` on the target server.

        :param executable: A dict containing the following parameters: {
            'host': 'The address of the server to connect to',
            'port': 'Server port to connect to',
            'database': 'The database name',
            'username': 'Database username',
            'password': 'Database user password',
            'script': 'Path to the script to execute',
        }
        :param properties: A Noora project properties instance
        """
        script = executable['script']

        cp = {
            'database': executable['database'],
        }
        if 'environment' in properties.keys():
            cp['environment'] = properties.get('environment')
        if 'previous' in properties.keys():
            cp['previous'] = properties.get('previous')

        stream = PreProcessor.parse(script, cp)

        tmp = File("tmp.sql")
        f = open(tmp.get_url(), 'w')
        f.write(stream)
        f.close()

        script_reader = open(tmp.get_url())

        feedback = File('feedback.log')
        feedback_writer = open(feedback.get_url(), 'w')

        statement = \
            "PGPASSWORD={passwd} psql -h {host} -p {port} -U {user} -d {db} " \
            "-v ON_ERROR_STOP=1".format(
                host=executable['host'],
                port=executable.get('port'),
                user=executable['username'],
                passwd=executable['password'],
                db=executable['database'],
            )

        call = CallFactory.new_call(statement)
        call['stdin'] = script_reader
        call['stdout'] = feedback_writer
        call['stderr'] = feedback_writer
        result = Shell.execute(call)
        self.set_result(result)

