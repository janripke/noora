.. Noora documentation master file, created by
   sphinx-quickstart on Thu Feb 21 13:32:40 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/noora.png
   :align: center

Welcome to Noora
================

Noora is a deployment tool that can be used to automate the database deployment cycle. It allows you to organize your database structure, do versioning on your data model, set up environments and generate self-contained Python packages that can deploy your structure to a server.

Noora was created with the DevOps paradigm in mind; especially when as a team you manage many database models it enables you to standardize your DDL and streamline development, testing, acceptance and deployment in production.

NOTE: This project is currently split across two branches, where Noora 1.1.0 provides MySQL and MSSQL support using Python 2 and 3 and Noora 1.0.2 supports Oracle and MySQL using Python 2 only. This documentation only describes Noora 1.1.


Quick Start
===========

To install Noora, you can either install a release from Github or install from source::

  # Install a release from Github
  $> pip install https://github.com/janripke/noora/archive/1.0.13.zip

  # Clone and install from source
  $> git clone https://github.com/janripke/noora/
  $> cd noora
  $> pip install .

We'll set up a MySQL project, so first make sure to create a user and database for your project::

  $> mysql -uroot
  mysql> create user hw@'localhost' identified by 'welcome123';
  mysql> grant all on hello_world.* to hw@'localhost';
  mysql> -- This is currently required to be able to drop functions and procedures, to be fixed
  mysql> grant select, delete on mysql.proc to hw@'localhost';
  mysql> flush privileges;

Then, on the command line create your project::

  database : hello_world
  host [localhost] :
  username : hw
  password : welcome123
  version [1.0.0]:
  version 1.0.0 created.

Add a table and some data to your newly created project::

  $> echo "CREATE TABLE hello ( value VARCHAR(128) );" > hello_world-db/create/hello_world/ddl/tab/hello.sql
  $> echo "INSERT INTO hello SET value='world';" > hello_world-db/create/hello_world/dat/hello.sql

Now, let's deploy the project and see what happens::

  $> mynoora create -h=localhost
  creating database 'hello_world' on host 'localhost' using environment 'dev'
  /home/niels/tmp/hello_world-db/create/hello_world/ddl/tab/application_properties.sql
  /home/niels/tmp/hello_world-db/create/hello_world/ddl/tab/hello.sql
  /home/niels/tmp/hello_world-db/create/hello_world/ddl/fct/get_property.sql
  /home/niels/tmp/hello_world-db/create/hello_world/ddl/trg/application_properties_bi.sql
  /home/niels/tmp/hello_world-db/create/hello_world/ddl/trg/application_properties_bu.sql
  /home/niels/tmp/hello_world-db/create/hello_world/ddl/idx/application_properties.sql
  /home/niels/tmp/hello_world-db/create/hello_world/dat/hello.sql
  /home/niels/tmp/hello_world-db/create/hello_world/dat/version.sql
  /home/niels/tmp/hello_world-db/create/hello_world/dat/dev/environment.sql
  database 'hello_world' created.

You can verify that the table you added along with some default data was deployed, and that the current version of your database model is 1.0.0 in the 'dev' environment::

  $> mysql -uhw -p
  Enter password:
  mysql> select * from hello;
  +--------+
  | value  |
  +--------+
  | world; |
  +--------+
  1 row in set (0.00 sec)

  mysql> select get_property('application.version');
  +-------------------------------------+
  | get_property('application.version') |
  +-------------------------------------+
  | 1.0.0                               |
  +-------------------------------------+
  1 row in set (0.00 sec)

That's it! To learn more about Noora projects, check out :ref:`getting_started`. For now, you can clear out your database like this::

  $> mynoora drop -h=localhost
  dropping database 'hello_world' on host 'localhost' using environment 'dev'
  /home/niels/projects/noora/noora/plugins/mysql/drop/vw/drop_views.sql
  /home/niels/projects/noora/noora/plugins/mysql/drop/tab/drop_tables.sql
  /home/niels/projects/noora/noora/plugins/mysql/drop/prc/drop_procedures.sql
  /home/niels/projects/noora/noora/plugins/mysql/drop/fct/drop_functions.sql
  database 'hello_world' dropped.

Note that this does not actually drop the database itself, rather it removes all objects, including views and procedures.


Documentation
=============

.. toctree::
   :maxdepth: 2

   getting_started
   plugin_reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
