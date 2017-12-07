#!/usr/bin/env python

import unittest

from noora.io.File import File
from noora.processor.PreProcessor import PreProcessor
from noora.shell.CallFactory import CallFactory
from noora.shell.Shell import Shell
from noora.system.Properties import Properties


class TestShell(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProcessor(self):
        script = File("drop_tables.sql")

        properties = Properties()
        properties.set_property('database', 'acme')

        stream = PreProcessor.parse(script, properties)
        tmp = File("tmp.sql")
        f = open(tmp.get_url(), 'w')
        f.write(stream)
        f.close()

        script_reader = open(tmp.get_url())

        feedback = File('feedback.log')
        feedback_writer = open(feedback.get_url(), 'w')

        statement = "mysql --host=localhost --user=apps --password=apps acme"
        call = CallFactory.new_call(statement)
        call['stdin'] = script_reader
        call['stdout'] = feedback_writer
        call['stderr'] = feedback_writer
        result = Shell.execute(call)



if __name__ == '__main__':
    unittest.main()
