# De versie's van de database
VERSIONS=['1.0.0']

# De schema's in de database
SCHEMES=['apps']

# De object typen die worden verwijderd.
# Dit zijn folders in de de drop boom.
# De volgorde is de volgorde waarin object typen worden verwijderd.
DROP_OBJECTS=['usr','vw','syn','trg','typ','tab','prc','fct','pkg','seq','idx','dbl']

# De object typen die worden aangemaakt door create of alter
# Dit zijn folder in de create en alter boom.
# De volgorde bepaalt de volgorde waarin de object typen worden aangemaakt.
CREATE_OBJECTS=['usr','dbl','dir','seq','syn','tab','cst','vw','prc','pkg','jar','trg','idx','gra']

# Bevat de verschillende schema's met hun omgevingen, gebruikersnaam en wachtwoord.
ORACLE_USERS=[['apps',['dev','test','uat','prod'],'apps','apps']]

# Deprecated
# DEFAULT_ORACLE_SID='orcl'

# Wanneer geen omgeving (environment) wordt opgegeven wordt deze omgeving gebruikt.
# Meestal is dit de development omgeving.
# De omgevingsvariabele bepaalt welke omgevingsspecifieke gegevens worden
# geladen, zie ook de dat boom in de alter en create folder.
DEFAULT_ENVIRONMENT='dev'

# Wordt gebruikt om het herbouwen (recreate) en het verwijderen (drop)
# voor specifieke omgevingen (environment) te blokkeren.
# Meestal is dit de produktie omgeving.
BLOCKED_ENVIRONMENTS=['prod','uat']

# Contains a list of oracle sids. Any given oracle sid must be in
# this list.
ORACLE_SIDS=['orcl']

# Contains a list of blocked oracle sids. 
# Blocked sids can not be dropped. 
# Normaly this variable contains the oracle sid of your production environment.
BLOCKED_ORACLE_SIDS=[]

CHECK_VERSION_SCHEMA='apps'

EXCLUDED_EXTENSIONS=['bak','~','pyc','log']

# Folders die niet worden gelezen
EXCLUDED_FOLDERS=['.svn','hotfix']

# Files die niet worden gelezen
EXCLUDED_FILES=['install.sql']

# Deze variabele wordt alleen gebruikt door het prepareer (prepare) script.
# De variabele bepaalt welke omgevings folders worden aangemaakt.
ENVIRONMENTS=['dev','test','uat','prod']

# Deze variabele wordt alleen gebruikt door het prepareer (prepare) script.
# De variabele bepaalt in welk schema het versie script wordt aangemaakt. 
VERSION_SCHEMA='apps'

VERSION_UPDATE_STATEMENT="update application_properties set value='<version>' where name='xx_log.version';"
VERSION_INSERT_STATEMENT="insert into application_properties(id,name,value) values (application_properties_s.nextval,'xx_log.version','1.0.0');"
VERSION_SELECT_STATEMENT="select value into l_value from application_properties where name='xx_log.version';"
ENVIRONMENT_INSERT_STATEMENT="insert into application_properties(id,name,value) values (application_properties_s.nextval,'database.environment','<environment>');"
ENVIRONMENT_SELECT_STATEMENT="select value into l_value from application_properties where name='database.environment';"

# Deze variabele wordt alleen gebruikt door het prepareer (prepare) script.
# De variabele bepaalt welke versie folder wordt aangemaakt in wijzig 
# (alter) folder wanneer er nog wijzigingen hebben plaatsgevonden.
DEFAULT_VERSION='1.0.1'

COMPONENT_UPDATE_STATEMENT="update application_properties set value='<version>' where name='<name>';"
COMPONENT_INSERT_STATEMENT="insert into application_properties(id,name,value) values (application_properties_s.nextval,'<name>','<version>');"



