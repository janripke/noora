#!/usr/bin/env python

import unittest
import os
import noora
from noora.connectors.MssqlConnector import MssqlConnector
from noora.io.File import File


class TestConnector(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEnvironment(self):
        noora_dir = os.path.dirname(noora.__file__)
        current_dir = os.path.abspath('.')

        properties = dict()
        properties["noora.dir"] = noora_dir
        properties["current.dir"] = current_dir

        executable = {}
        executable['script'] = File("exec_get_environment.sql")
        executable['host'] = "elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433"
        executable['user'] = "Elsevier"
        executable['password'] = "Elsevier144"
        executable['database'] = "ElsevierDB"

        connector = MssqlConnector()
        connector.execute(executable, properties)

    def testMssqlConnector(self):
        noora_dir = os.path.dirname(noora.__file__)
        current_dir = os.path.abspath('.')

        properties = dict()
        properties["noora.dir"] = noora_dir
        properties["current.dir"] = current_dir

        executable = {}
        executable['script'] = File("drop_application_properties_s.sql")
        executable['host'] = "elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433"
        executable['user'] = "Elsevier"
        executable['password'] = "Elsevier144"
        executable['database'] = "ElsevierDB"

        connector = MssqlConnector()
        connector.execute(executable, properties)


        executable = {}
        executable['script'] = File("application_properties_s.sql")
        executable['host'] = "elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433"
        executable['user'] = "Elsevier"
        executable['password'] = "Elsevier144"
        executable['database'] = "ElsevierDB"

        connector = MssqlConnector()
        connector.execute(executable, properties)

        executable = {}
        executable['script'] = File("drop_application_properties.sql")
        executable['host'] = "elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433"
        executable['user'] = "Elsevier"
        executable['password'] = "Elsevier144"
        executable['database'] = "ElsevierDB"

        connector = MssqlConnector()
        connector.execute(executable, properties)


        executable = {}
        executable['script'] = File("application_properties.sql")
        executable['host'] = "elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433"
        executable['user'] = "Elsevier"
        executable['password'] = "Elsevier144"
        executable['database'] = "ElsevierDB"

        connector = MssqlConnector()
        connector.execute(executable, properties)

        executable = {}
        executable['script'] = File("drop_app_prop.sql")
        executable['host'] = "elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433"
        executable['user'] = "Elsevier"
        executable['password'] = "Elsevier144"
        executable['database'] = "ElsevierDB"

        connector = MssqlConnector()
        connector.execute(executable, properties)


        executable = {}
        executable['script'] = File("app_prop.sql")
        executable['host'] = "elsevierdb4.c07v9zv3jhxs.eu-west-1.rds.amazonaws.com,1433"
        executable['user'] = "Elsevier"
        executable['password'] = "Elsevier144"
        executable['database'] = "ElsevierDB"

        connector = MssqlConnector()
        connector.execute(executable, properties)
            

if __name__ == '__main__':
    unittest.main()
