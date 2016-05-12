import ConfigNG

is_special = lambda k,v: (k.startswith('__') and \
   k.endswith('__')) or type(v) == type(__builtins__)

def do_module(m):
   return [k for k,v in m.__dict__.iteritems() if not is_special(k,v)]

fd = open('ConfigNG.rst', 'w')


fd.write( """
ConfigNG Package
================

:mod:`ConfigNG` Package
-----------------------

.. automodule:: ConfigNG.__init__

""" )


for f in do_module(ConfigNG):
   if f.endswith('Error'):
      fd.write( '.. autoclass:: %s\n' % (f,) )
      fd.write( '   :show-inheritance:\n\n' )
   else:
      fd.write( '.. autofunction:: %s\n\n' % (f,) )


fd.write( """
:mod:`api` Module
-----------------

.. automodule:: ConfigNG.api

""")

for f in do_module(ConfigNG.api):
   fd.write( '.. autofunction:: %s\n\n' % (f,) )


fd.write( """
:mod:`configcont` Module
------------------------

.. automodule:: ConfigNG.configcont

.. autoclass:: ConfigCont
   :members:
   :special-members:
   :show-inheritance:

""")


fd.write( """
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

""" )

from restgrid import make_grid

fixds = lambda s:' '.join(s.splitlines())

fd.write( make_grid( [('type', 'description')] + [(k, fixds(v.__doc__)) for k,v in ConfigNG.types.types.iteritems()] ) + '\n')

fd.close()
