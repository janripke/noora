#!/usr/bin/env python

import unittest
import os
import noora
from noora.connectors.MssqlConnector import MssqlConnector
from noora.system.Properties import Properties
from noora.io.File import File


class TestConnector(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEnvironment(self):
        noora_dir = os.path.dirname(noora.__file__)
        current_dir = os.path.abspath('.')

        properties = Properties()
        properties.set_property("noora.dir", noora_dir)
        properties.set_property("current.dir", current_dir)

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

        properties = Properties()
        properties.set_property("noora.dir", noora_dir)
        properties.set_property("current.dir", current_dir)

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


      # properties = Properties()
      # propertyLoader = PropertyLoader(properties)
      # file = File("project.conf")
      # fileReader = FileReader(file)
      # propertyLoader.load(fileReader)
      #
      # properties.setProperty("noora.dir", NOORA_DIR)
      # properties.setProperty("noora.script.dir", NOORA_DIR + os.sep + 'scripts')
      #
      # connector = OracleConnector()
      # execute = ExecuteFactory.newOracleExecute()
      # execute.setHost('orcl')
      # execute.setUsername('apps')
      # execute.setPassword('apps')
      # file = File('application_properties.sql')
      # execute.setScript(file)
      #
      # connector.execute(execute, properties)
      #
            

if __name__ == '__main__':
    unittest.main()
