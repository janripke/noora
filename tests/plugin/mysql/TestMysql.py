#!/usr/bin/env python
import unittest
from noora.mynoora_cli import main


class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        # assuming using host = localhost, user = apps , database = acme

        # # drop the acme database
        # args = ['drop', '-h', 'localhost']
        # main(args)
        #
        # # create the acme database
        # args = ['create', '-h', 'localhost']
        # main(args)
        #
        # # update the acme database to version 1.0.1
        # args = ['update', '-h', 'localhost', '-v', '1.0.1']
        # main(args)
        #
        # # update the acme database to version 1.0.2
        # args = ['update', '-h', 'localhost', '-v', '1.0.2']
        # main(args)

        # recreate the acme database up to the latest version
        args = ['recreate', '-h', 'localhost']
        main(args)

        # show help
        args = ['help']
        main(args)


if __name__ == '__main__':
    unittest.main()
