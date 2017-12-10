#!/usr/bin/env python
import unittest

from noora.io.File import File
from noora.processor.PreProcessor import PreProcessor
from noora.system.Properties import Properties


class TestPreProcessor(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProcessor(self):
        script = File("drop_tables.sql")

        properties = Properties()
        properties.set_property('database', 'orcl')

        stream = PreProcessor.parse(script, properties)
        self.assertEqual(stream, 'orcl', "invalid transformation")


if __name__ == '__main__':
    unittest.main()
