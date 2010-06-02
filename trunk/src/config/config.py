# De schema's in de database
SCHEMAS=['<schemas>']

# De object typen die worden verwijderd.
# Dit zijn folders in de de drop boom.
# De volgorde is de volgorde waarin object typen worden verwijderd.
DROP_OBJECTS=['usr','vw','syn','trg','typ','tab','prc','jar','fct','pkg','seq','idx','dbl']

# De object typen die worden aangemaakt door create of alter
# Dit zijn folder in de create en alter boom.
# De volgorde bepaalt de volgorde waarin de object typen worden aangemaakt.
CREATE_OBJECTS=['usr','dbl','dir','seq','syn','tab','cst','vw','prc','pkg','jar','trg','idx','gra']

# Bevat de verschillende schema's met hun omgevingen, gebruikersnaam en wachtwoord.
ORACLE_USERS=[['<schema>',['dev','test','uat','prod'],'<oracle_user>','<oracle_passwd>']]

# Wanneer geen oracle_sid wordt opgegeven wordt deze sid gebruikt.
# Meestal is dit de oracle_sid van de development omgeving.
DEFAULT_ORACLE_SID='<default_oracle_sid>'

# Wanneer geen omgeving (environment) wordt opgegeven wordt deze omgeving gebruikt.
# Meestal is dit de development omgeving.
# De omgevingsvariabele bepaalt welke omgevingsspecifieke gegevens worden
# geladen, zie ook de dat boom in de alter en create folder.
DEFAULT_ENVIRONMENT='<default_environment>'

# Wordt gebruikt om het herbouwen (recreate) en het verwijderen (drop)
# voor specifieke omgevingen (environment) te blokkeren.
# Meestal is dit de produktie omgeving.
BLOCKED_ENVIRONMENTS=['<blocked_environment>','<blocked_environment>']

# Hier wordt het schema opgegeven wat de database versie bevat.
CHECK_VERSION_SCHEMA='<version_schema>'

# Bevat de bestandstypen die worden geexecuteerd
EXCLUDED_EXTENSIONS=['.bak','.~','.pyc','.log']

# Folders die niet worden gelezen
EXCLUDED_FOLDERS=['.svn','hotfix']


# Deze variabele wordt alleen gebruikt door het prepareer (prepare) script.
# De variabele bepaalt welke omgevings folders worden aangemaakt.
ENVIRONMENTS=['dev','test','uat','prod']

# Deze variabele wordt alleen gebruikt door het prepareer (prepare) script.
# De variabele bepaalt in welk schema het versie script wordt aangemaakt. 
VERSION_SCHEMA='<version_schema>'

# Hieronder de sql statements voor ophalen, toevoegen en lezen van de database versie en omgeving.
VERSION_UPDATE_STATEMENT="update application_properties set value='<version>' where name='xx_log.version';"
VERSION_INSERT_STATEMENT="insert into application_properties(id,name,value) values (application_properties_s.nextval,'xx_log.version','1.0.0');"
VERSION_SELECT_STATEMENT="select value into l_value from application_properties where name='xx_log.version';"
ENVIRONMENT_INSERT_STATEMENT="insert into application_properties(id,name,value) values (application_properties_s.nextval,'database.environment','<environment>');"
ENVIRONMENT_SELECT_STATEMENT="select value into l_value from application_properties where name='database.environment';"

# Deze variabele wordt alleen gebruikt door het prepareer (prepare) script.
# De variabele bepaalt welke versie folder wordt aangemaakt in wijzig 
# (alter) folder wanneer er nog wijzigingen hebben plaatsgevonden.
DEFAULT_VERSION='1.0.1'

# Deze variabele wordt gebruikt om aan te geven dat deze database wordt gebruikt voor het onderhouden
# van een component en bevat de naam van het component.
# Een component kan worden gebruikt in andere database. 
# Met behulp van het script build_component.py kan een component worden aangemaakt. 
# Deze variabele wordt alleen gebruikt in de database waar het component wordt onderhouden.
COMPONENT_NAME='<component_name>'

# Deze variabele geeft de initiele versie aan van het component.
# Deze variabele wordt alleen gebruikt in de database waar het component wordt onderhouden.
COMPONENT_CREATE_VERSION='1.0.0'

# Deze variabele geeft aan welke bestanden uit de component database GEEN onderdeel gaan uitmaken
# van het component.
# Deze variabele wordt alleen gebruikt in de database waar het component wordt onderhouden.
COMPONENT_EXCLUDED_FILES=['version.sql','build.py']

# Deze variabele geeft aan in welke folder het component wordt geplaatst.
# Deze variabele wordt alleen gebruikt in de database waar het component wordt onderhouden.
COMPONENT_RELEASE_FOLDER='releases'

# Deze variabele geeft aan welk update statement wordt gebruikt voor het bijwerken van de versie.
# Deze variabele komt alleen voor in de database(s) waar componenten worden gebruikt.
COMPONENT_UPDATE_STATEMENT="update application_properties set value='<version>' where name='<name>';"

# Deze variabele geeft aan welk insert statement wordt gebruikt voor het bijwerken van de versie.
# Deze variabele komt alleen voor in de database(s) waar componenten worden gebruikt.
COMPONENT_INSERT_STATEMENT="insert into application_properties(id,name,value) values (application_properties_s.nextval,'<name>','<version>');"



