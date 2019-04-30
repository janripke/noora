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

Inside the create directory you'll find another directory, one for every database (or schema) that is managed by your project. If you just generated your project, there'll be only one database, in our example called "acme".

In this example, there are two subdirectories: ``dat`` and ``ddl``. The ``dat`` directory contains static data for your database. For example, per environment you deploy your database to you can set environment specific settings.

In the ``ddl`` directory, the real source code for your database is stored, separated by object type, for example:

* `fct` - Database functions;
* `idx` - Index definitions;
* `prc` - Stored procedures;
* `tab` - Table definitions;
* `trg` - Triggers;

.. NOTE::

  The ``ddl`` subdirectories vary per plugin and are documented in :ref:`plugin_reference`. They are also fully customizable. The directories described in the documentation are just default values, you are free to create your own directory structure and amend the ``create_objects`` and ``drop_objects`` directives in your project configuration accordingly.


Project Settings
----------------

The ``myproject.json`` file is the core of a project's configuration in noora. It is a single configuration file that contains the majority of information required to build a project the way you want.

An example configuration for MySQL looks like this::

  {
    "project": "acme",
    "databases": [
      "apps"
    ],
    "aliasses": [],
    "database_aliases" : [],
    "mysql_users": [
      [
        "localhost",
        "acme",
        "apps",
        "Welcome123",
        "3306"
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
      "fct",
      "trg",
      "idx"
    ],
    "technology": "mysql"
  }


Below is the list of configuration directives in ``myproject.json`` that are common across all technologies, grouped together by context:

Generic Configuration Directives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below directives are specific to the target infrastructure:

* **project**: The name of the project
* **technology**: The database technology of this project. This is used to determine which plugins to load, among other things;
* **{technology}_hosts**: A list of hosts the project may be deployed to;
* **blocked_hosts**: A list of hosts to block when running destructive operations such as the *drop* plugin;
* **{technology}_users**: A list of tuples containing authentication information for every database or schema in your project. See :ref:`plugin_reference` for specifications of these tuples;

Target environment
^^^^^^^^^^^^^^^^^^

The next directives are related to the environment you deploy your database in, for example when your projects have testing, acceptance and production setups, you can use the environments directives:

* **environments**: The list of environments your database can be deployed in;
* **default_environment**: The default environment that Noora will operate on if not explicitly specified.
* **environment_insert_statement**: The statement to run to set the environment a new database was deployed to;
* **environment_select_statement**: The statement to run to look up the environment for a database;

Versioning
^^^^^^^^^^

Versioning directives. These are normally set by the *generate* plugin and generally do not need to be changed:

* **default_version**: The initial version of your project. This version will be inserted in the properties table when running the *create* plugin;
* **version_database**: Which database (or schema) should be used when manipulating version properties. A project should have only one database containing the properties table;
* **version_insert_statement**: The statement to run after creating a new database, setting the initial database version;
* **version_update_statement**: The statement that will be run after deploying a new version to your database;
* **version_select_statement**: The statement run for getting the current version of a database.

File inclusion and exclusion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A number of directives related to including or excluding files and directories when running Noora plugins:

* **create_objects**: When running the *create* plugin, only SQL scripts in these directories will be executed inside the Project's create directory;
* **drop_objects**: When running the *drop* plugin, run all SQL scripts in these directories (NOTE: these scripts are included in the drop plugin package directory);

.. NOTE::

  The order of items in the create and drop objects lists is important. If you change your directory setup, make sure that a proper execution order is observed (i.e.: dropping functions before their referenced tables).

Excluding files:

* **excluded_extensions**: Files with an extension from this list will be ignored;
* **excluded_folders**: Files where the folder path matches a folder in this list will be ignored;
* **excluded_files**: Files that match a filename in this list will be ignored.

----

For more on technologies, plugins and technology-specific directives, continue reading in :ref:`plugin_reference`.
