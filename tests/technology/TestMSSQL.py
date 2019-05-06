#!/usr/bin/env python
import os
import shutil
import unittest

from subprocess import check_output

from noora.exceptions.plugins.InvalidVersionException import InvalidVersionException

from TestScenario import get_suite, TechnologyFullSimpleTest


TEST_DIR = '/tmp'
TEST_DB = {
    'name': 'noora_test_mssql',
    'host': '127.0.0.1',
    'port': 1433,
    'user': 'apps',
    'pass': 'Welcome123',
}


class TestMSSQLBase(TechnologyFullSimpleTest):
    """
    Base class for setting up and tearing down a MSSQL technology test.
    """
    def __init__(self, *args, **kwargs):
        TechnologyFullSimpleTest.__init__(self, *args, **kwargs)
        self.update_settings(TEST_DIR, TEST_DB)

    def setUp(self):
        """
        Set up a MySQL noora project after asserting it doesn't exist in the test dir.
        """
        # FIXME: create database and assign permissions

        os.chdir(self.test_dir)
        self.assertFalse(os.path.exists('{}/{}-db'.format(self.test_dir, self.test_db)))

        cmd = [
            'mynoora', 'generate', 'mssql',
            '-h', '{}'.format(self.test_db['host']),
            '-p', '{}'.format(self.test_db['port']),
            '-d', self.test_db['name'],
            '-s', self.test_db['name'],
            '-U' '{}'.format(self.test_db['user']),
            '-P', '{}'.format(self.test_db['pass']),
            '-v', '1.0.0',
        ]

        check_output(cmd)

    def tearDown(self):
        """Destroy the project files"""
        # Try to drop the database
        try:
            check_output(['mynoora', 'drop', '-h', self.test_db['host']])
        except InvalidVersionException:
            pass

        shutil.rmtree('{}/{}-db'.format(self.test_dir, self.test_db['name']))


suite = get_suite(TestMSSQLBase)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite)
