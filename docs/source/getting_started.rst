.. _getting_started:

Getting Started
===============

In this part we'll introduce you to Noora, how to prepare your database for usage with Noora, and outline the Command Line Interface.


Why Noora?
----------

To Do:

* Philosophy of programmatic databases (integrate parts of white paper)
* Explanation of interaction with db through command line tools


Database Support and Requirements
---------------------------------

Noora currently supports MySQL, MSSQL and PostgreSQL databases. Support for Oracle is in the process of being migrated into the new codebase. Support for Teradata will follow soon.

For every technology there are some requirements and preparations you must carry out before you can use Noora with your database of choice. We'll explain every technology in turn.

MySQL
^^^^^

For any host you will run Noora on, the minimal requirement is to have installed the ``mysql`` command line client. Generally on Linux distributions, the package will be called ``mysql-client``.

On your database instance, all that is required is a user that has sufficient rights to interact with the database you want Noora to manage for you. You provide login details for this user when you create the project later on.

Suppose you want to run your project inside a database called ``acme``, using a user called ``apps``, with your database running on the local machine, you need to run the following commands::

  CREATE DATABASE acme;
  CREATE USER apps@'localhost' IDENTIFIED BY 'Welcome123';
  GRANT ALL ON acme.* TO apps@'localhost';
  -- This is currently required to be able to drop functions and procedures, to be fixed
  GRANT SELECT, DELETE ON mysql.proc TO apps@'localhost';
  FLUSH PRIVILEGES;

.. NOTE::

  Procedures and functions in MySQL are manipulated through mysql scripting and queries, but the ``PREPARE`` syntax does not support dropping these objects at this moment, making removing them directly from ``mysql.proc`` the only option. For this reason, your database user needs select and delete rights on this table. We are working on a solution for this.

Microsoft SQL Server
^^^^^^^^^^^^^^^^^^^^

To use Noora with Microsoft SQL Server, having the ``sqlcmd`` commandline utility installed is required. You can find installation instructions here for Windows, Linux and MacOS:

* Windows: https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility?view=sql-server-2017
* Linux & MacOS: https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools?view=sql-server-2017

Next, you'll need to configure all schemas you want to manage through Noora with one user that has full access to these schemas::

  -- First create a login on the DB instance. In this case we use a SQL server login
  -- but other login types are of course possible
  CREATE LOGIN apps WITH PASSWORD='Welcome123';
  -- Make sure the target database is selected
  USE acme;
  -- Now create a database user for the login you just created
  CREATE USER apps FOR LOGIN apps;
  -- Create the target schema and assign the required rights to the db user
  CREATE SCHEMA acme AUTHORIZATION apps GRANT CONTROL ON SCHEMA::acme TO apps;
  ALTER USER apps with DEFAULT_SCHEMA=acme;
  ALTER ROLE db_ddladmin ADD MEMBER apps;

.. NOTE::

  Noora's Microsoft SQL plugins support managing multiple schemas in your database. However, the generate plugin does not yet support selecting a specific schema outside of the user's default schema. We will implement a fix for this soon.

PostgreSQL
^^^^^^^^^^

For PostgreSQL, you'll need the client installed on any system you run Noora from. Generally, packages will be called ``postgresql-client-X.Y`` where X.Y is the version of the target PostgreSQL instance.

Then, for your project, set up a database, user and permissions like such::

  CREATE DATABASE acme;
  CREATE USER apps WITH ENCRYPTED PASSWORD 'Welcome123';
  GRANT ALL ON DATABASE acme TO apps;


The Noora CLI
-------------

To create and manage your Noora projects, you can use the command line interface ``mynoora``. The CLI has two operating modes: inside a project's scope and outside a project's scope; when running Noora, the CLI will determine if you executed the command from inside a project folder, and make a different set of commands available depending on the context.


The Command Structure
^^^^^^^^^^^^^^^^^^^^^

Right now, you have yet to create a Noora project, so if you run Noora, you'll get something like this::

  $ mynoora
  Usage: mynoora [OPTIONS] COMMAND [ARGS]...

    NoOra is a database deployment tool used to automate the database
    deployment cycle.

  Options:
    -r, --revision  Report the version of Noora and exit.
    --help          Show this message and exit.

  Commands:
    generate  The generate plugin can be used to create a new database
              project...

As you can see, only ``generate`` is available as a command. To see which technologies are available to create projects for, run::

  $ mynoora generate --help
  Usage: mynoora generate [OPTIONS] COMMAND [ARGS]...

    The generate plugin can be used to create a new database project or
    bootstrap a new version for the currently selected project.

  Options:
    --help  Show this message and exit.

  Commands:
    mssql  Generate a new MSSQL database project
    mysql  Generate a new MySQL database project

Suppose you want to create a MySQL database, you can check out the options like so::

  $ mynoora generate mysql --help
  Usage: mynoora generate mysql [OPTIONS]

    Generate a new MySQL database project

  Options:
    -h, --host TEXT
    -p, --port INTEGER
    -d, --database TEXT  [required]
    -U, --username TEXT  [required]
    -P, --password TEXT  [required]
    -v, --version TEXT
    --help               Show this message and exit.


Creating a new project
^^^^^^^^^^^^^^^^^^^^^^

There are two ways to create a project: interactive or using options. If you simply run ``mynoora generate mysql``, the CLI will prompt you for all options, including a non-echoing password prompt and confirmation prompt. But, for example, if you want to be able to generate projects unattended, you can simply provide all the options on the command line!

For now, we'll generate a MySQL project using options::

  $ mynoora generate mysql -h localhost -p 3306 -d acme -U apps -P Welcome123 -v 1.0.0
  version 1.0.0 created.

What does this do? The generate script creates a project directory for you, suffixed with "-db". You are free to rename this directory.

Inside the project, a configuration file is created called ``myproject.json``, storing the details you just provided along with the project default settings. Secondly, one directory is added containing the initial project files for you database.

----

The project configuration and structure are described in the next section: :ref:`working_with_projects`.
