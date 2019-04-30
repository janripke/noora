API
===

Core
----

System: CLI
^^^^^^^^^^^
.. automodule:: noora.system.App
    :members:

.. automodule:: noora.system.GenerateCommand
    :members:

System
^^^^^^
.. automodule:: noora.system.Properties
    :members:

.. automodule:: noora.system.Ora
    :members:

.. automodule:: noora.system.ClassLoader
    :members:


Utilities
---------

Database interaction
^^^^^^^^^^^^^^^^^^^^

Base classes for database connectivity. For implementations, see :ref:`plugin_reference`.

.. automodule:: noora.connectors.Connectable
    :members:

.. automodule:: noora.connectors.Connector
    :members:

.. automodule:: noora.connectors.ConnectionExecutor
    :members:

Version tools
^^^^^^^^^^^^^

Utilities for version checking and manipulation.

.. automodule:: noora.version.Version
    :members:

.. automodule:: noora.version.Versions
    :members:

.. automodule:: noora.version.VersionLoader
    :members:

.. automodule:: noora.version.VersionGuesser
    :members:

Shell tools
^^^^^^^^^^^

Functionality for interacting with the shell. Mainly used by connectors.

.. automodule:: noora.shell.Shell
    :members:

.. automodule:: noora.shell.CallFactory
    :members:

.. automodule:: noora.shell.StartupInfoFactory
    :members:

Template processing
^^^^^^^^^^^^^^^^^^^

.. automodule:: noora.processor.PreProcessor
    :members:

Argument checking
^^^^^^^^^^^^^^^^^

Mainly used by plugins to check plugin arguments against the project settings.

.. automodule:: noora.plugins.Fail
    :members:

File utilities
^^^^^^^^^^^^^^

To be expanded.

.. automodule:: noora.io.File
    :members:

