.. _getting_started:

Getting Started
===============

In this section we'll introduce you to Noora, how to prepare your database for usage with Noora, and outline the Command Line Interface.

Why Noora?
----------

To Do:

* Philosophy of programmatic databases (integrate parts of white paper)
* Explanation of interaction with db through command line tools

Database Support and Requirements
---------------------------------

Noora currently supports MySQL and MSSQL databases. Support for Oracle is in the process of being migrated into the new codebase. Support for Teradata and PostgreSQL will follow soon.

For every technology there are some requirements and preparations you must carry out before you can use Noora with your database of choice. We'll explain every technology in turn.

MySQL
^^^^^

For any host you will run Noora on, the minimal requirement is to have installed the ``mysql`` command line client. Generally on Linux distributions, the package will be called ``mysql-client``.

On your database instance, all that is required is a user that has sufficient rights to interact with the database you want Noora to manage for you. You provide login details for this user when you create the project later on.

Suppose you want to run your project inside a database called ``acme``, using a user called ``apps``, with your database running on the local machine, you need to run the following commands::

  $> mysql -uroot
  mysql> create database acme;
  mysql> create user apps@'localhost' identified by 'secret';
  mysql> grant all on acme.* to apps@'localhost';
  mysql> -- This is currently required to be able to drop functions and procedures, to be fixed
  mysql> grant select, delete on mysql.proc to apps@'localhost';
  mysql> flush privileges;


.. NOTE::

  Procedures and functions in MySQL are manipulated through mysql scripting and queries, but the ``PREPARE`` syntax does not support dropping these objects at this moment, making removing them directly from ``mysql.proc`` the only option. For this reason, your database user needs select and delete rights on this table. We are working on a solution for this.


Microsoft SQL Server
^^^^^^^^^^^^^^^^^^^^


The Noora CLI
-------------
