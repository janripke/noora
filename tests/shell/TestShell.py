#!/usr/bin/env python

import unittest

from noora.io.File import File
from noora.processor.PreProcessor import PreProcessor
from noora.shell.CallFactory import CallFactory
from noora.shell.Shell import Shell


class TestShell(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCheckVersion(self):
        script = File("checkversion.sql")

        properties = dict()
        properties['name'] = 'app_prop'
        properties['previous'] = '1.0.0'

        stream = PreProcessor.parse(script, properties)
        tmp = File("tmp.sql")
        f = open(tmp.get_url(), 'w')
        f.write(stream)
        f.close()

        script_reader = open(tmp.get_url())

        feedback = File('feedback.log')
        feedback_writer = open(feedback.get_url(), 'w')

        statement = "mysql --show-warnings --host=localhost --user=apps --password=apps acme"
        call = CallFactory.new_call(statement)
        call['stdin'] = script_reader
        call['stdout'] = feedback_writer
        call['stderr'] = feedback_writer
        result = Shell.execute(call)
        print("result", result)


if __name__ == '__main__':
    unittest.main()
