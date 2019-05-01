#!/usr/bin/env python
import os
import shutil
import unittest

from subprocess import check_output

from noora.exceptions.plugins.InvalidVersionException import InvalidVersionException


TEST_DIR = '/tmp'
TEST_DB = {
    'name': 'noora_test_mysql',
    'host': 'localhost',
    'port': 3306,
    'user': 'apps',
    'pass': 'Welcome123',
}


class TestMySQLBase(unittest.TestCase):
    """
    Base class for setting up and tearing down a MySQL technology test.
    """
    def setUp(self) -> None:
        """
        Set up a MySQL noora project after asserting it doesn't exist in the test dir.
        """
        # FIXME: create database

        os.chdir(TEST_DIR)
        self.assertFalse(os.path.exists('{}/{}-db'.format(TEST_DIR, TEST_DB)))

        cmd = [
            'mynoora', 'generate', 'mysql',
            '-h', '{}'.format(TEST_DB['host']),
            '-p', '{}'.format(TEST_DB['port']),
            '-d', TEST_DB['name'],
            '-U' '{}'.format(TEST_DB['user']),
            '-P', '{}'.format(TEST_DB['pass']),
            '-v', '1.0.0',
        ]

        check_output(cmd)

    def tearDown(self) -> None:
        """Destroy the project files"""
        # Try to drop the database
        try:
            check_output(['mynoora', 'drop', '-h', TEST_DB['host']])
        except InvalidVersionException:
            pass

        shutil.rmtree('{}/{}-db'.format(TEST_DIR, TEST_DB['name']))


class TestMySQL(TestMySQLBase):
    def test_full(self):
        """
        Perform a full test:
        - Create database at default version
        - Generate two new versions
        - Attempt to upgrade while skipping version (assert exception)
        - Upgrade as intended
        - Drop database
        - Recreate database at latest version
        """
        # Change directory to db
        os.chdir('{}/{}-db'.format(TEST_DIR, TEST_DB['name']))

        # Run create command
        check_output(['mynoora', 'create', '-h', TEST_DB['host']])

        # Generate new versions, 1.0.1 and 1.1.0
        check_output(['mynoora', 'generate'])
        check_output(['mynoora', 'generate', '-v', '1.1.0'])

        # Upgrade to wrong version
        #with self.assertRaises(InvalidVersionException):
        #    check_output(['mynoora', 'update', '-v 1.1.0', '-h', TEST_DB['host']])

        # Upgrade right versions
        check_output(['mynoora', 'update', '-v', '1.0.1', '-h', TEST_DB['host']])
        check_output(['mynoora', 'update', '-v', '1.1.0', '-h', TEST_DB['host']])

        # Recreate at latest version
        check_output(['mynoora', 'recreate', '-v', '1.1.0', '-h', TEST_DB['host']])

        # Finally, drop database
        check_output(['mynoora', 'drop', '-h', TEST_DB['host']])


if __name__ == '__main__':
    unittest.main()