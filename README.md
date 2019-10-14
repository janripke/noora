# ![noora logo](https://a.fsdn.com/allura/p/noora/icon)


# Welcome to Noora
Noora is a deployment tool for automating the database deployment cycle. It allows you to organize your database structure, do versioning on your data model, set up environments and generate self-contained Python packages that can deploy your structure to a server.

Noora was created with the DevOps paradigm in mind; especially when as a team you manage many database models it enables you to standardize your DDL and streamline development, testing, acceptance and deployment in production.

NOTE: This project is currently split across two branches, where Noora 1.1.0 provides MySQL and MSSQL support using Python 2 and 3 and Noora 1.0.2 supports Oracle and MySQL using Python 2 only. This documentation describes Noora >= 1.1.

Noora is released under the [GNU General Public License](LICENSE).


# Quick Start
To install Noora, you can install from pip, a release from Github or from source::

```
# Install from PyPi
$ pip install noora

# Install from github
$ pip install git+https://github.com/janripke/noora.git@1.1.6#egg=noora

# Clone and install from source
$ git clone https://github.com/janripke/noora/
$ cd noora
# Checkout the release you want to use 
# (NOTE: the master branch is NOT guaranteed to be stable!)
$ git checkout tags/1.1.6
$ pip install .
```

We'll set up a MySQL project, so first make sure to create a user and database for your project:

```
$> mysql -uroot
mysql> create database acme;
mysql> create user apps@'localhost' identified by 'apps';
mysql> grant all on acme.* to apps@'localhost';
mysql> -- This is currently required to be able to drop functions and procedures, to be fixed
mysql> grant select, delete on mysql.proc to apps@'localhost';
mysql> flush privileges;
```

Then, on the command line create your project:

```
$ mynoora generate -t=mysql
Host [localhost]:
Port [3306]:
Database name: acme
Database username: apps
Database password:
Repeat for confirmation:
Initial project version [1.0.0]:
version 1.0.0 created.
```

Add a table and some data to your newly created project:

```
$ echo "CREATE TABLE hello ( value VARCHAR(128) );" > acme-db/create/acme/ddl/tab/hello.sql
$ echo "INSERT INTO hello SET value='world';" > acme-db/create/acme/dat/hello.sql
```

Now, let's deploy the project and see what happens:

```
$ cd acme-db
$ mynoora create -h=localhost
creating database 'acme' on host 'localhost' using environment 'dev'
/home/niels/tmp/acme-db/create/acme/ddl/tab/application_properties.sql
/home/niels/tmp/acme-db/create/acme/ddl/tab/hello.sql
/home/niels/tmp/acme-db/create/acme/ddl/fct/get_property.sql
/home/niels/tmp/acme-db/create/acme/ddl/trg/application_properties_bi.sql
/home/niels/tmp/acme-db/create/acme/ddl/trg/application_properties_bu.sql
/home/niels/tmp/acme-db/create/acme/ddl/idx/application_properties.sql
/home/niels/tmp/acme-db/create/acme/dat/hello.sql
/home/niels/tmp/acme-db/create/acme/dat/version.sql
/home/niels/tmp/acme-db/create/acme/dat/dev/environment.sql
database 'acme' created.
```

You can verify that the table you added along with some default data was deployed, and that the current version of your database model is 1.0.0 in the 'dev' environment: 

```
$ mysql -uapps -p acme
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
```

That's it! To learn more about Noora projects, check out http://noora.readthedocs.org/getting-started. For now, you can clear out your database like this::

```
$ mynoora drop -h=localhost
dropping database 'acme' on host 'localhost' using environment 'dev'
/home/niels/projects/noora/noora/plugins/mysql/drop/vw/drop_views.sql
/home/niels/projects/noora/noora/plugins/mysql/drop/tab/drop_foreign_keys.sql
/home/niels/projects/noora/noora/plugins/mysql/drop/prc/drop_procedures.sql
/home/niels/projects/noora/noora/plugins/mysql/drop/fct/drop_functions.sql
database 'acme' dropped.
```

Note that this does not actually drop the database itself, rather it removes all objects, including views and procedures.


# Next Steps

Check out the documentation over at http://noora.readthedocs.org/
