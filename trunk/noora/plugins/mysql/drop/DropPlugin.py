#!/usr/bin/env python
from noora.plugins.Plugin import Plugin
from noora.plugins.Fail import Fail
from noora.plugins.mysql.drop.BlockedHostException import BlockedHostException
from noora.system.PropertyHelper import PropertyHelper
from noora.system.Ora import Ora
from noora.connectors.ConnectionExecutor import ConnectionExecutor
from noora.connectors.MysqlConnector import MysqlConnector
from noora.io.File import File
import os


class DropPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, "drop", MysqlConnector())

    def get_drop_dir(self, properties):
        return os.path.join(properties.get_property('plugin.dir'), 'mysql', 'drop')

    def fail_on_blocked_hosts(self, host, properties):
        blocked_hosts = properties.get_property('blocked_hosts')
        if host in blocked_hosts:
            message = "block host " + host
            raise BlockedHostException(message)

    def execute(self, arguments, properties):
        host = arguments.h
        Fail.fail_on_no_host(host)
        self.fail_on_blocked_hosts(host, properties)

        default_databases = properties.get_property('databases')
        databases = Ora.nvl(arguments.d, default_databases)
        Fail.fail_on_invalid_database(arguments.d, properties)

        default_environment = properties.get_property('default_environment')
        environment = Ora.nvl(arguments.e, default_environment)
        Fail.fail_on_invalid_environment(arguments.e, properties)

        objects = properties.get_property('drop_objects')

        alias = arguments.a
        Fail.fail_on_invalid_alias(arguments.a, properties)

        # if an alias is given, only the alias database will be installed, other databases will be ignored.
        if alias:
            print "using alias :" + alias
            databases = [alias]

        for database in databases:
            print "dropping database '" + database + "' on host '" + host + "' using environment '" + environment + "'"

            users = properties.get_property('mysql_users')
            username = PropertyHelper.get_mysql_user(users, host, database)
            password = PropertyHelper.get_mysql_passwd(users, host, database)

            connector = self.get_connector()

            executor = {}
            executor['host'] = host
            executor['database'] = database
            executor['username'] = username
            executor['password'] = password

            for object in objects:
                folder = File(os.path.join(self.get_drop_dir(properties), object))
                ConnectionExecutor.execute(connector, executor, properties, folder)

            print "database '" + database + "' dropped."
