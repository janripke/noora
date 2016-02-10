#!/usr/bin/env python
import os

from org.noora.cl.OptionFactory import OptionFactory
from org.noora.connector.ConnectorFactory import ConnectorFactory
from org.noora.connector.ExecuteFactory import ExecuteFactory
from org.noora.io.File import File
from org.noora.io.Files import Files
from org.noora.io.Path import Path
from org.noora.plugin.ConnectionExecutor import ConnectionExecutor
from org.noora.plugin.Plugin import Plugin


class TripolisDeployEmailPlugin(Plugin):
    __revision__ = "$Revision$"

    def __init__(self):
        Plugin.__init__(self, "TRIPOLIS:DEPLOY:EMAIL", ConnectorFactory.newTripolisDeployEmailConnector())

    def getDescription(self):
        return "deploys all emails to Tripolis"

    def getOptions(self, properties):
        options = Plugin.getOptions(self)
        options.addOption("-?", "--help", False, False, "display help")

        option = OptionFactory.newOption("-w", "--workspace", True, True, "deploy emails to this workspace")
        option.setValues(properties.getPropertyValues('WORKSPACES'))
        options.add(option)

        option = OptionFactory.newOption("-e", "--environment", True, False, "deploy emails to this environment")
        option.setValues(properties.getPropertyValues('ENVIRONMENTS'))
        options.add(option)

        option = OptionFactory.newOption("-v", "--version", True, True, "version of emails to deploy")
        options.add(option)

        return options

    def execute(self, commandLine, properties):
        defaultWorkspace = properties.getPropertyValues('DEFAULT_WORKSPACE')
        workspace = commandLine.getOptionValue('-w', defaultWorkspace)
        defaultEnvironment = properties.getPropertyValues('DEFAULT_ENVIRONMENT')
        environment = commandLine.getOptionValue('-e', defaultEnvironment)
        version = commandLine.getOptionValue('-v')

        connector = self.getConnector()

        folder = File(Path.path(os.path.abspath('.'),version))

        for directEmailType in Files.list(folder):
            print "Creating '"+directEmailType.getName()+"' emails, using environment '"+environment+"'"
            executor = ExecuteFactory.newTripolisExecute()
            executor.setWorkspace(workspace)
            executor.setDiretEmailType(directEmailType.getName())

            # global email objects
            ConnectionExecutor.execute(connector, executor, properties, directEmailType)

            # environment specific email objects
            ConnectionExecutor.execute(connector, executor, properties,
                                       File(Path.path(directEmailType.getPath(), directEmailType.getName(), environment)))
            print "'"+directEmailType.getName()+"' emails created."