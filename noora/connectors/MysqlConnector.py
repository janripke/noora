from noora.io.File import File
from noora.shell.Shell import Shell
from noora.shell.CallFactory import CallFactory

from noora.connectors.Connector import Connector
from noora.processor.PreProcessor import PreProcessor


class MysqlConnector(Connector):
    """
    Connector for MySQL server.
    """
    def execute(self, executable, properties):
        """
        Execute the script provided by `executable` on the target server.

        :type executable: dict
        :param executable: Should contain the following keys and values:

            * **host**: The address of the server to connect to;
            * **port**: Server port to connect to;
            * **database**: The database name;
            * **username**: Database username;
            * **password**: Database user password;
            * **script**: Path to the script to execute.
        :type properties: noora.system.Properties.Properties
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

        statement = "mysql --show-warnings --port={port} --host={host} --user={user} " \
                    "--password={passwd} {db}".format(
                        host=executable['host'],
                        port=executable.get('port') or '3306',
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

