
from org.noora.plugin.Plugin import Plugin

class DatabasePlugin(Plugin):

  def __init__(self, plugintype, connector):
    Plugin.__init__(self, plugintype, connector)
        