.. _plugin_reference:

Plugin Reference
================

This page documents per technology the default object structure, technology-specific configuration directives and all available plugins.

MySQL
-----

Objects and directives
^^^^^^^^^^^^^^^^^^^^^^

A Noora MySQL project can contain one or more databases inside one MySQL instance. When creating a MySQL project, you'll get the following ddl objects for your initial database, in order of execution (the ``create_objects`` directive):

* **tab**: Tables are stored here. A table ``application_properties`` is added by Noora to manage project properties;
* **fct**: Contains functions. A ``get_property`` function is added by Noora to manage project properties;
* **trg**: Contains triggers. Triggers are added by Noora to manage insert and update actions on the project properties table;
* **idx**: Contains indexes. An index for the ``application_properties`` table is added by Noora.

The ``drop_objects`` directive has the following default list, in order of execution:

* vw
* trg
* tab
* prc
* fct
* idx

The MySQL technology also supports using aliases for your database. Add an alias to the ``aliasses`` (sic) list in ``myproject.json`` to enable the alias, and add a mapping to the ``database_aliases`` list to map a database to an alias, e.g.: ``"database_aliases": [(foo, foo_bar)]``.

Plugins
^^^^^^^

.. autoclass:: noora.plugins.mysql.generate.GeneratePlugin.GeneratePlugin
    :members:

.. autoclass:: noora.plugins.mysql.create.CreatePlugin.CreatePlugin
    :members:

.. autoclass:: noora.plugins.mysql.drop.DropPlugin.DropPlugin
    :members:

.. autoclass:: noora.plugins.mysql.update.UpdatePlugin.UpdatePlugin
    :members:

.. autoclass:: noora.plugins.mysql.recreate.RecreatePlugin.RecreatePlugin
    :members:


Microsoft SQL
-------------

Objects and directives
^^^^^^^^^^^^^^^^^^^^^^

A Microsoft SQL Server project contains one or more schemas inside one MSSQL Database Instance. When creating a MSSQL project, you'll get the following ddl objects for your initial database, in order of execution (the ``create_objects`` directive):

* **seq**: Contains sequences. A sequence for the ``application_properties`` table is added by Noora;
* **syn**: FIXME
* **tab**: Tables are stored here. A table ``application_properties`` is added by Noora to manage project properties;
* **cst**: FIXME
* **fct**: Contains functions. A ``get_property`` function is added by Noora to manage project properties;
* **prc**: Contains stored procedures.
* **vw**: Contains views.
* **trg**: Contains triggers. Triggers are added by Noora to manage insert and update actions on the project properties table;
* **idx**: Contains indexes. An index for the ``application_properties`` table is added by Noora.
* **gra**: FIXME

The ``drop_objects`` directive has the following default list, in order of execution:

* vw
* syn
* typ
* tab
* prc
* fct
* seq
* idx
* dbl

Plugins
^^^^^^^

.. autoclass:: noora.plugins.mssql.generate.GeneratePlugin.GeneratePlugin
    :members:

.. autoclass:: noora.plugins.mssql.create.CreatePlugin.CreatePlugin
    :members:

.. autoclass:: noora.plugins.mssql.drop.DropPlugin.DropPlugin
    :members:

.. autoclass:: noora.plugins.mssql.update.UpdatePlugin.UpdatePlugin
    :members:

.. autoclass:: noora.plugins.mssql.recreate.RecreatePlugin.RecreatePlugin
    :members:


PostgreSQL
----------

Objects and directives
^^^^^^^^^^^^^^^^^^^^^^

Plugins
^^^^^^^


Adding Plugins
--------------

To Do.
