.. _working_with_projects:

Working with Projects
=====================

As explained in :ref:`getting_started`, when you run the Noora CLI, there are two contexts; one where you are outside a project directory and can generate new projects, the other context is where you work inside a project directory.

In this section we'll explain the project directory structure and how versioning works inside the project. Next we'll explain the ``myproject.json`` settings file and its directives.


The Project Directory
---------------------

The MySQL generate plugin created the following standard project structure::

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

At the top level resides the project settings file along with the ``create`` directory. This directory contains the initial version of your project and will always be looked in first when deploying to an empty database.

Inside the create directory you'll find another directory, one for every database that is managed by your project. If you just generated your project, there'll be only one database, in our example called "acme".

In this example, there are two subdirectories: `dat` and `ddl`. The `dat` directory contains static data for your database. For example, per environment you deploy your database to you can set environment specific settings.

In the `ddl` directory, the real source code for your database is stored, separated by object type, for example:

* `fct` - Database functions;
* `idx` - Index definitions;
* `prc` - Stored procedures;
* `tab` - Table definitions;
* `trg` - Triggers;

.. NOTE::

  The `ddl` subdirectories vary per plugin and are documented in :ref:`plugin_reference`.


Project Settings
----------------

The ``myproject.json`` file is the core of a project's configuration in noora. It is a single configuration file that contains the majority of information required to build a project the way you want.

An example configuration for MySQL looks like this::

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


Generic Configuration Directives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

FIXME
