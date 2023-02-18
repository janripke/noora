#!/usr/bin/env python
import unittest
from noora.mynoora_cli import main
from noora.plugins.mysql.drop.drop_plugin import DropPlugin
from noora.plugins.mysql.create.create_plugin import CreatePlugin
from noora.connectors.mysql_connector_stub import MysqlConnectorStub
from noora.system.app import App


class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCommandLinePass(self):
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

    def testDropPass(self):
        # retrieve the basic properties.
        properties = App.properties()

        # load the properties from the myproject.json file.
        App.load_properties(properties)

        # retrieve the basic mynoora parser.
        parser = App.get_parser()
        args = ['drop', '-h', 'localhost']

        plugin = DropPlugin()
        arguments = plugin.parse_args(parser, args)
        plugin.set_connector(MysqlConnectorStub())
        plugin.execute(arguments, properties)

    def testCreatePass(self):
        # retrieve the basic properties.
        properties = App.properties()

        # load the properties from the myproject.json file.
        App.load_properties(properties)

        # retrieve the basic mynoora parser.
        parser = App.get_parser()
        args = ['create', '-h', 'localhost']

        plugin = CreatePlugin()
        arguments = plugin.parse_args(parser, args)
        plugin.set_connector(MysqlConnectorStub())
        plugin.execute(arguments, properties)


if __name__ == '__main__':
    unittest.main()
