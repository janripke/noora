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

        tmp = StringIO()
        tmp.write(stream)
        tmp.seek(0)

        feedback = File('feedback.log')
        feedback_writer = open(feedback.get_url(), 'w')

        statement = "PGPASSWORD={passwd} psql -h {host} -p {port} -U {user} -d {db}".format(
            host=executable['host'],
            port=executable.get('port'),
            user=executable['username'],
            passwd=executable['password'],
            db=executable['database'],
        )

        call = CallFactory.new_call(statement)
        call['stdin'] = tmp
        call['stdout'] = feedback_writer
        call['stderr'] = feedback_writer
        result = Shell.execute(call)
        self.set_result(result)

