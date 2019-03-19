.. _working_with_projects:

Working with Projects
=====================

The Project Folder
------------------

The generate plugin created the following standard project structure::

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

You will also notice that the generate plugin created the acme directory.
This folder is called the database folder.

The create/acme/dat directory contains the project data scripts.
The create/acme/ddl directory contains the source code.
The myproject.json file in the root of the database project is the project's project configuration file.


myproject.json
--------------
The myproject.json file is the core of a project's configuration in noora. It is a single configuration file that contains the majority of information required to build a project in just the way you want.
This project's myproject.json looks like this::

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
