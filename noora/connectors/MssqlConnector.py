from noora.io.File import File
from noora.shell.Shell import Shell
from noora.shell.CallFactory import CallFactory

from noora.processor.PreProcessor import PreProcessor
from noora.connectors.Connector import Connector


class MssqlConnector(Connector):
    """
    Connector for Microsoft SQL server.
    """
    def execute(self, executable, properties):
        """
        Execute the script provided by `executable` on the target server.

        :type executable: dict
        :param executable: Should contain the following keys and values:

            * **host**: The address of the server to connect to;
            * **port**: Server port to connect to;
            * **database**: The database name;
            * **schema**: The schema to use;
            * **username**: Database username;
            * **password**: Database user password;
            * **script**: Path to the script to execute.
        :type properties: noora.system.Properties.Properties
        :param properties: A Noora project properties instance
        """
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

