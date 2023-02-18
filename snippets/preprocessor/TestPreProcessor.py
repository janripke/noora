#!/usr/bin/env python
import unittest

from noora.io.file import File
from noora.processor.pre_processor import PreProcessor


class TestPreProcessor(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProcessor(self):
        script = File("drop_tables.sql")

        properties = dict()
        properties['database'] = 'orcl'

        stream = PreProcessor.parse(script, properties)
        self.assertEqual(stream, 'orcl', "invalid transformation")


if __name__ == '__main__':
    unittest.main()
