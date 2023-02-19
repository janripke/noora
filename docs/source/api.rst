API
===

Core
----

System: CLI
^^^^^^^^^^^
.. automodule:: noora.system.app
    :members:

.. automodule:: noora.system.generate_command
    :members:

System
^^^^^^
.. automodule:: noora.system.properties
    :members:

.. automodule:: noora.system.ora
    :members:

.. automodule:: noora.system.class_loader
    :members:


Utilities
---------

Database interaction
^^^^^^^^^^^^^^^^^^^^

Base classes for database connectivity. For implementations, see :ref:`plugin_reference`.

.. automodule:: noora.connectors.connectable
    :members:

.. automodule:: noora.connectors.connector
    :members:

.. automodule:: noora.connectors.connection_executor
    :members:

Version tools
^^^^^^^^^^^^^

Utilities for version checking and manipulation.

.. automodule:: noora.version.version
    :members:

.. automodule:: noora.version.versions
    :members:

.. automodule:: noora.version.version_loader
    :members:

.. automodule:: noora.version.version_guesser
    :members:

Shell tools
^^^^^^^^^^^

Functionality for interacting with the shell. Mainly used by connectors.

.. automodule:: noora.shell.shell
    :members:

.. automodule:: noora.shell.call_factory
    :members:

.. automodule:: noora.shell.startup_info_factory
    :members:

Template processing
^^^^^^^^^^^^^^^^^^^

.. automodule:: noora.processor.pre_processor
    :members:

Argument checking
^^^^^^^^^^^^^^^^^

Mainly used by plugins to check plugin arguments against the project settings.

.. automodule:: noora.plugins.fails
    :members:

File utilities
^^^^^^^^^^^^^^

To be expanded.

.. automodule:: noora.io.file
    :members:

