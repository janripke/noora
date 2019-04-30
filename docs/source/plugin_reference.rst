.. _plugin_reference:

Plugin Reference
================

This page documents per technology the default object structure, technology-specific configuration directives and all available plugins.

The plugin structure is kept disconnected from the command line interface so it can be easily integrated into other projects. Plugin objects are initialized context-free, meaning you have to pass around configuration and arguments. However, this means you can easily chain plugins and reuse them across projects if you so desire.

In the last section we have included documentation about extending plugins or adding technologies.

Plugin Base Class
^^^^^^^^^^^^^^^^^

.. autoclass:: noora.plugins.Plugin.Plugin
    :members:


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

Connector and Plugins
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: noora.connectors.MysqlConnector.MysqlConnector
    :members:

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

Connector and Plugins
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: noora.connectors.MssqlConnector.MssqlConnector
    :members:

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

A PostgreSQL Server project contains one or more schemas inside one PostgreSQL Database. When creating a  project, you'll get the following ddl objects for your initial database, in order of execution (the ``create_objects`` directive):

* **seq**: Contains sequences. A sequence for the ``application_properties`` table is added by Noora;
* **tab**: Tables are stored here. A table ``application_properties`` is added by Noora to manage project properties;
* **fct**: Contains functions. A ``get_property`` function is added by Noora to manage project properties;
* **vw**: Contains views.
* **trg**: Contains triggers. Triggers are added by Noora to manage insert and update actions on the project properties table;
* **idx**: Contains indexes. An index for the ``application_properties`` table is added by Noora.

The ``drop_objects`` directive has the following default list, in order of execution:

* vw
* trg
* fct
* tab
* idx
* sex

Connector and Plugins
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: noora.connectors.PGSQLConnector.PGSQLConnector
    :members:

.. autoclass:: noora.plugins.postgresql.generate.GeneratePlugin.GeneratePlugin
    :members:

.. autoclass:: noora.plugins.postgresql.create.CreatePlugin.CreatePlugin
    :members:

.. autoclass:: noora.plugins.postgresql.drop.DropPlugin.DropPlugin
    :members:

.. autoclass:: noora.plugins.postgresql.update.UpdatePlugin.UpdatePlugin
    :members:

.. autoclass:: noora.plugins.postgresql.recreate.RecreatePlugin.RecreatePlugin
    :members:


Adding Plugins or Technologies
------------------------------

Creating plugins
^^^^^^^^^^^^^^^^

Adding a plugin is fairly easy:

1. Add a package for your plugin by creating ``noora.plugins.<technology>.<plugin_name>.__init__.py``;
2. Add a plugin class in the module ``noora.plugins.<technology>.<plugin_name>.<PluginName>Plugin`` called ``<PluginName>Plugin``;
3. Make sure your plugin class subclasses the technology's base plugin class (generally called ``noora.plugins.<technology>.<Technology>Plugin.<Technology>Plugin);``
4. Lastly, your plugin should have an ``execute()`` method that accepts two parameters: ``properties`` and ``arguments`` which should be of type ``noora.system.Properties.Properties`` and ``dict`` respectively.

The execute method does not need to return anything and should raise exceptions where applicable.

To enable the new plugin to be called from the command line, make sure to create a ``cli`` method inside the plugin package root (``noora.plugins.<technology>.<plugin_name>``). This method can be a simple click command.

By naming the command ``cli``, it is automatically discovered by the Noora CLI. If your plugin is also usable outside a project scope, you can create a ``cli_outside_scope`` command in the plugin package root.

Make sure to add the ``@click.pass_obj`` decorator. This will enable the CLI to pass the properties object to the command, which you can in turn pass on to your plugin.


Adding technologies
^^^^^^^^^^^^^^^^^^^

Adding a technology starts by creating a package inside the ``noora.plugins`` package with the name of your new technology. Then, you'll need to fulfill the following requirements:

* Add a connector for your technology. See ``noora.connectors`` for examples;
* Add a technology base plugin that inherits ``noora.plugins.Plugin.Plugin`` and configures the proper connector to use;
* Add a ``generate`` plugin for the technology with templates for the project configuration and default objects to create. NOTE: the generate plugin should be able to create a new project as well as a new version inside a project;
* Add the minimally required ``create``, ``drop`` and ``update`` plugins. The ``recreate`` plugin is not required but recommended to implement.
