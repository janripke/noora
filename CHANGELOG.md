Changelog
=========

**NOTE**: We're currently migrating Noora to a new structure. This changelog describes changes in the `noora` package as found in the root of this project. The old code resides in `src` and will not receive updates.

Version 1.2.8
-------------
* module naming conform python standards
* mssql, added connection-string support
* mssql, added tests

Version 1.2.7
-------------
* postgresql, changed the deploy and recreate plugin, support for the keyword latest is added to the version parameter.

Version 1.2.6
-------------
* postgresql, connection-string support, to avoid adding database credentials database project.


Version 1.2.0 
-------------
* changed layout connection parameters, sections mysql_users, mssql_users and postgresql users
  was a list is now a dictionary. You have to change your old configurations
  ```json
  "mssql_users": [
    {
      "host": "{host}",
      "schema": "{schema}",
      "username": "{username}",
      "password": "{password}",
      "port": "{port}"
    }
  ],
  
  "mysql_users": [
    {
      "host": "{host}",
      "database": "{database}",
      "username": "{username}",
      "password": "{password}",
      "port": "{port}"
    }
  ],
  
  "postgresql_users": [
    {
      "host": "{host}",
      "database": "{database}",
      "username": "{username}",
      "password": "{password}",
      "port": "{port}"
    }
  ],
```


Version 1.1.1
-----------------------
New features:

* Refactor of mynoora_cli.py, App.py and GeneratePlugin.py to use click library;
* Add cli method to all plugin init files with appropriate options;
* Added simple tests for testing main plugins of technologies
* Add support for PostgreSQL (technology, connector, plugins, documentation)

Improvements and fixes:

* Move repeating code from Connector subclasses upstream;
* Move all exceptions into their own package;
* Update Fail functionality with additional checks, improve string checks, make exception messages more informative;
* Add technology plugin classes;
* Split up all plugins into preparation and execution phase, where preparation handles input arguments;
* Change myproject.json templates with some bugfixes and new defaults;
* Improvements to finding and loading plugin classes.
* Updates to documentation, with more information about commands, the project structure and project configuration;
* Change imports in plugins to be absolute where applicable (in places relative imports were used)
* Remove support for specifiying schema for MSSQL and PostgreSQL; operations should always be performed on all schemas/databases considering that version management applies to the entire project (MySQL still to do, but aliases make it trickier)
* Expand on documentation: getting started, working with projects, plugin reference, API
* Add A LOT of docstrings in the code;


Version 1.1.0 (released 2019-03-01)
-----------------------------------
Changes in this release (https://github.com/janripke/noora/releases/tag/1.1.0):

* Make Noora (the new version) Python 3 compatible
* Add Sphinx documentation in preparation of merging and migrating all documentation into the repository and into Readthedocs
* Add support for specifying non-standard ports for MySQL and MSSQL databases
* Bring the code up to PEP-8 spec
* Move exceptions into a separate package and fix all references