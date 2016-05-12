
ConfigNG Package
================

:mod:`ConfigNG` Package
-----------------------

.. automodule:: ConfigNG.__init__

.. autofunction:: get_config

.. autoclass:: ConfigParserError
   :show-inheritance:


:mod:`api` Module
-----------------

.. automodule:: ConfigNG.api

.. autofunction:: is_container

.. autofunction:: has_type

.. autofunction:: add_type

.. autofunction:: get_type

.. autofunction:: add_container

.. autofunction:: has_container


:mod:`configcont` Module
------------------------

.. automodule:: ConfigNG.configcont

.. autoclass:: ConfigCont
   :members:
   :special-members:
   :show-inheritance:


:mod:`factories` Module
-----------------------

.. automodule:: ConfigNG.factories
   :members:
   :show-inheritance:


:mod:`errors` Module
--------------------

.. automodule:: ConfigNG.errors
   :members:
   :undoc-members:
   :show-inheritance:


Included validators
-------------------
ConfigValueError or ConfigTypeError is raised if the input is invalid.

+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|type    |description                                                                                                                                                                                    |
+========+===============================================================================================================================================================================================+
|notype  |anything goes!                                                                                                                                                                                 |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|str     |stringiness is obligatory                                                                                                                                                                      |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|bool    |value may be "true" or "false", evaluates to Python boolean values True and False                                                                                                              |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|int     |digits and negative sign only. will not convert a decimal value!                                                                                                                               |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|fp      |passed straight into float() built-in function                                                                                                                                                 |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|path    |leading part of path must exist, and the last element be a valid directory    entry. symbolic links are followed                                                                               |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|epath   |an existing directory entry (file, directory, or perhaps something else).                                                                                                                      |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|dir     |an existing directory.                                                                                                                                                                         |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|file    |an existing file.                                                                                                                                                                              |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|userport|nonpriviledged port numbers, 1024-65535                                                                                                                                                        |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|platmixd|an existing directory, chosen from a pair, depending on platform.    Takes two newline delimited directories and returns the first when    not run under windows, otherwise returns the second.|
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|platmixf|an existing file, chosen from a pair, depending on platform.    Takes two newline delimited files and returns the first when    not run under windows, otherwise returns the second.           |
+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
