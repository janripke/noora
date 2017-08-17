from org.noora.plugin.tripolis.generate.TripolisGenerateEmailPlugin import TripolisGenerateEmailPlugin


plugin = TripolisGenerateEmailPlugin()

moduleName = 'org.noora.plugin.mysql.create.CreatePlugin'
mod = __import__(moduleName ,globals(), locals(), [''])