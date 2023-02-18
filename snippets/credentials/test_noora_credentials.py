from os.path import expanduser
from noora.system import property_helper
import os
import json
from noora.io.files import Files


properties = dict()
properties['home.dir'] = expanduser('~')


home_dir = properties.get('home.dir')

credentials = os.path.join(home_dir, '.noora', 'credentials.json')

# create the .noora folder if not exists
if not os.path.isdir(os.path.dirname(credentials)):
    os.makedirs(os.path.dirname(credentials))

# create .noora/credentials if not exists
if not os.path.isfile(credentials):
    f = open(credentials, 'w')
    f.close()

# use credentials
f = open(credentials, 'r')
credentials = json.load(f)

# resolve the name of the project, which is in myproject.json
project = "acme-db"

profile = credentials.get(project)
mysql_users = None
if profile:
    mysql_users = profile.get('mysql_users')

databases = ['acme']
host = 'localhost'

for database in databases:
    executor = PropertyHelper.get_mysql_properties(mysql_users, host, database)
    print(executor['username'])

