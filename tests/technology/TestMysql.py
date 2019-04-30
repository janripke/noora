#!/usr/bin/env python
import os
import shutil
import unittest

from subprocess import check_output


TEST_DIR = '/tmp'
TEST_DB = 'noora-test-mysql'


class TestMySQLBase(unittest.TestCase):
    """
    Base class for setting up and tearing down a MySQL technology test.
    """
    def setUp(self) -> None:
        os.chdir(TEST_DIR)
        self.assertFalse(os.path.exists('{}/{}-db'.format(TEST_DIR, TEST_DB)))

        cmd = [
            'mynoora',
            'generate',
            'mysql',
            '-h localhost',
            '-p 33060',
            '-d', 'noora-test-mysql',
            '-U apps',
            '-P Welcome123',
            '-v 1.0.0',
        ]
        check_output(cmd)

    def tearDown(self) -> None:
        shutil.rmtree('{}/{}-db'.format(TEST_DIR, TEST_DB))


class TestMySQL(TestMySQLBase):
    def test_001(self):
        pass

    def test_002(self):
        pass


if __name__ == '__main__':
    unittest.main()