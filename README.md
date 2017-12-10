noora
## ![noora logo](https://a.fsdn.com/allura/p/noora/icon)
========

NoOra is a database deployment tool which can be used to automate the database deployment cycle and is designed for agile and or devops teams.
The supported database platforms are Oracle and Mysql.

# Installation
Noora currently supports Python 2.x

## Install release
Enter the following to install noora on your system.
In this example noora version 1.0.5 is installed.

```
$ pip install git+https://github.com/janripke/noora.git@1.0.5#egg=noora --upgrade
```

## Install from source using virtualenv

First, clone the repo on your machine and then install with `pip`:

```
$ git clone https://github.com/janripke/noora
$ cd noora
$ virtualenv env
$ source env/bin/activate
$ pip install .
```

## Check that the installation worked

Simply run : 
```
$ mynoora help
NoOra a database deployment tool.
https://github.com/janripke/noora
1.0.5-SNAPSHOT
```

# Create your first mysql database project

In this example it is assumed that you have installed a mysql database server.

## Create the mysql database user

Enter the following commands to create the database user apps in the mysql server.
This action is seen as a administrator task and is done once.

```
$ mysql --user=root --password=[password]
mysql> CREATE USER 'apps'@'localhost' IDENTIFIED BY 'apps';
mysql> GRANT ALL PRIVILEGES ON * . * TO 'apps'@'localhost'
mysql> flush privileges;
mysql> exit
```

## Create the mysql database

Enter the following commands to create the database acme in the mysql server.
This action is seen as a administrator task and is done once.

```
$ mysql --user=apps --password=[password]
mysql> create database acme;
```

## Create the database project.

Execute the following commands to create a new database project.

```
$ mynoora generate
database : acme
host [localhost] :
username : apps
password : apps
version [1.0.0] :
version 1.0.0 created.
```

You will notice that the generate plugin created a directory with the name acme-db. 
Change into that directory.

```
$ cd acme-db
```

The generate plugin created the following standard project structure
```
acme-db
|-- myproject.json
`-- create
    |-- acme
    |   `-- dat
    |       `-- dev
    |           `-- environment.sql
    |       `-- prod
    |           `-- environment.sql
    |       `-- test
    |           `-- environment.sql
    |       `-- uat
    |           `-- environment.sql
    |       `-- version.sql
    |   `-- ddl
    |       `-- cst
    |       `-- fct
    |           `-- get_property.sql
    |       `-- idx
    |           `-- application_properties.sql
    |       `-- prc
    |       `-- tab
    |           `-- application_properties.sql
    |       `-- trg
    |           `-- application_properties_bi.sql
    |           `-- application_properties_bu.sql
    |       `-- vw
```

You will also notice that the generate plugin created the acme directory.
This folder is called the database folder.

The create/acme/dat directory contains the project data scripts. 
The create/acme/ddl directory contains the source code.
The myproject.json file in the root of the database project is the project's project configuration file.

### myproject.json
The myproject.json file is the core of a project's configuration in noora. It is a single configuration file that contains the majority of information required to build a project in just the way you want.
This project's myproject.json looks like this:

```
{
  "databases": [
    "acme"
  ],
  "aliasses": [],
  "database_aliases" : [],
  "mysql_users": [
    [
      "localhost",
      "acme",
      "apps",
      "apps"
    ]
  ],
  "default_environment": "dev",
  "mysql_hosts": [
    "localhost"
  ],
  "blocked_hosts": [],
  "version_database": "acme",
  "excluded_extensions": [
    "bak",
    "~",
    "pyc",
    "log"
  ],
  "excluded_folders": [
    ".svn",
    "hotfix"
  ],
  "excluded_files": [
    "install.sql"
  ],
  "environments": [
    "dev",
    "test",
    "uat",
    "prod"
  ],
  "version_update_statement": "update application_properties set value='<version>' where name='application.version';",
  "version_insert_statement": "insert into application_properties(name,value) values ('application.version','<version>');",
  "version_select_statement": "select value into l_value from application_properties where name='application.version';",
  "environment_insert_statement": "insert into application_properties(name,value) values ('application.environment','<environment>');",
  "environment_select_statement": "select value into l_value from application_properties where name='application.environment';",
  "default_version": "1.0.0",
  "drop_objects": [
    "vw",
    "trg",
    "tab",
    "prc",
    "fct",
    "idx"
  ],
  "create_objects": [
    "tab",
    "cst",
    "fct",
    "prc",
    "vw",
    "trg",
    "idx"
  ],
  "plugins": [
    "noora.plugins.mysql.generate.GeneratePlugin.GeneratePlugin",
    "noora.plugins.mysql.help.HelpPlugin.HelpPlugin",
    "noora.plugins.mysql.drop.DropPlugin.DropPlugin",
    "noora.plugins.mysql.create.CreatePlugin.CreatePlugin",
    "noora.plugins.mysql.update.UpdatePlugin.UpdatePlugin"
  ]
}
```

### What did i just do
You executed the noora plugin generate. The generate plugin created the database project folder, the project tree and initiated the myproject.json file.

## Install the database project into the mysql database server.
To install the database project into the mysql database server enter the following command:

```
$ mynoora create -h=localhost
```
The command line will print out various actions, the following is shown.
```
creating database 'acme' on host 'localhost' using environment 'dev'
/home/user/acme-db/create/acme/ddl/tab/application_properties.sql
/home/user/acme-db/create/acme/ddl/fct/get_property.sql
/home/user/acme-db/create/acme/ddl/trg/application_properties_bi.sql
/home/user/acme-db/create/acme/ddl/trg/application_properties_bu.sql
/home/user/acme-db/create/acme/ddl/idx/application_properties.sql
/home/user/acme-db/create/acme/dat/version.sql
/home/user/acme-db/create/acme/dat/dev/environment.sql
database 'acme' created.
```

## Remove the database project from the mysql database server.
To remove the database project from the mysql database server enter the following command:

```
$ mynoora drop -h=localhost
```

The command line will print out various actions, the following is shown.

```
dropping database 'acme' on host 'localhost' using environment 'dev'
/home/user/workspace/noora/noora/plugins/mysql/drop/vw/drop_views.sql
/home/user/workspace/noora/noora/plugins/mysql/drop/tab/drop_tables.sql
/home/user/workspace/noora/noora/plugins/mysql/drop/prc/drop_procedures.sql
/home/user/workspace/noora/noora/plugins/mysql/drop/fct/drop_functions.sql
database 'acme' dropped.
```

# License
Released under the [GNU General Public License](LICENSE).
