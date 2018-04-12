
# statement = ['loadjava', '-user', 'apps/apps@devel', '-resolve', '-force', '/home/user/workspace/noora/examples/oracle/loadjava/create/apps/ddl/jar/jtar.jar']
# executeList=['loadjava','-user',connectString, '-resolve', '-force', projectHelper.cleanPath(oracleScript)]
#       #templateScript='@'+projectHelper.cleanPath(self.getScriptDir()+os.sep+'template.sql')
#       print executeList
#       result=subprocess.call(executeList,shell=True,stdout=handle,stderr=handle,startupinfo=startupInfo)

from subprocess import Popen, PIPE

statement = 'loadjava -user apps/apps@devel -resolve -force /home/user/workspace/noora/examples/oracle/loadjava/create/apps/ddl/jar/jtar.jar'
p = Popen([statement], stdout=PIPE, shell=True)
output, error = p.communicate()
print error

