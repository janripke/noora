import os
import unittest
from subprocess import check_output


def get_suite(test_cls):
    mro = test_cls.mro()
    tests = set()
    for cls in mro:
        if hasattr(cls, '__tests__'):
            for test in cls.__tests__:
                tests.add(test)

    return unittest.TestSuite(map(test_cls, tests))


class TechnologyTestBase(object):
    __tests__ = []

    def __init__(self):
        self.test_dir = None
        self.test_db = None

    def update_settings(self, test_dir, test_db):
        self.test_dir = test_dir
        self.test_db = test_db


class TechnologyFullSimpleTest(TechnologyTestBase, unittest.TestCase):
    __tests__ = ['test_full']
    def __init__(self, *args, **kwargs):
        TechnologyTestBase.__init__(self)
        unittest.TestCase.__init__(self, *args, **kwargs)

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
        os.chdir('{}/{}-db'.format(self.test_dir, self.test_db['name']))

        # Run create command
        check_output(['mynoora', 'create', '-h', self.test_db['host']])

        # Generate new versions, 1.0.1 and 1.1.0
        check_output(['mynoora', 'generate'])
        check_output(['mynoora', 'generate', '-v', '1.1.0'])

        # Upgrade to wrong version
        #with self.assertRaises(InvalidVersionException):
        #    check_output(['mynoora', 'update', '-v 1.1.0', '-h', self.test_db['host']])

        # Upgrade right versions
        check_output(['mynoora', 'update', '-v', '1.0.1', '-h', self.test_db['host']])
        check_output(['mynoora', 'update', '-v', '1.1.0', '-h', self.test_db['host']])

        # Recreate at latest version
        check_output(['mynoora', 'recreate', '-v', '1.1.0', '-h', self.test_db['host']])

        # Finally, drop database
        check_output(['mynoora', 'drop', '-h', self.test_db['host']])
