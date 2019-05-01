#!/usr/bin/env python
import unittest

from TestMysql import suite as mysql_suite
from TestPostgreSQL import suite as psql_suite


if __name__ == "__main__":
    full_suite = unittest.TestSuite([mysql_suite, psql_suite])
    runner = unittest.TextTestRunner()
    runner.run(full_suite)