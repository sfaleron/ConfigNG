
"""Direct access is not intended; instead use the api module."""

from errors import *

from collections import OrderedDict

# "l" is implicit
containers = {}

types = OrderedDict()

def add_container(key, constructor, additem=None):
   """Add a container type. The container is considered immutable if additem is omitted or None.
   Raises ConfigTypeError if the type is invalid or additem isn't a method."""
   if '_' in key:
      raise ConfigTypeError('container name may not contain underscores')

   if key in ('l',):
      raise ConfigTypeError('may not override a reserved container')

   if additem:
      cont = constructor()
      if not hasattr(cont, additem) or not callable(getattr(cont, additem)):
         raise ConfigTypeError('"%s" not a method of the container' % (additem,))

   containers[key] = (constructor, additem)

def has_container(s):
   """True if passed a recognized container """
   return s == 'l' or s in containers

def add_type(s, validator):
   """Add a type. May override most existing types.
   Raises ConfigValueError if type is reserved or invalid,
   and ConfigTypeError if it's not a string.
   The validator is not, umm, validated."""
   if not isinstance(s, basestring):
      raise ConfigTypeError('type must be a string')

   if '_' in s:
      raise ConfigValueError('type name may not contain underscores')

   if s in ():
      raise ConfigTypeError('may not override a reserved type')

   types[s] = validator

def get_type(s):
   """For chaining/inheritence.
   Raises ConfigKeyError if the type is not recognized."""
   if not s in types:
      raise ConfigKeyError('unrecognized item type "%s"' % (s,))

   return types[s]

add_container('t', tuple)
add_container('f', frozenset )
add_container('s', set, 'add')


class TypeHelper(object):
   def __init__(self, s):
      if s is None:
         cont_type = None
         item_type = None
      else:
         if not isinstance(s, basestring):
            raise ConfigTypeError('type must be a string')

         if '_' in s:
            cont_type, item_type = s.split('_')
         else:
            cont_type = None
            item_type = s

      if cont_type and not cont_type in containers and cont_type != 'l':
         raise ConfigTypeError('unrecognized container type "%s"' % (cont_type,))

      if not item_type in types and item_type not in ('str', None):
         raise ConfigTypeError('unrecognized item type "%s"' % (item_type,))

      self.cont_type = cont_type
      self.item_type = item_type

      if cont_type and cont_type != 'l':
         self.constructor, self.additem = containers[cont_type]

   def is_container(self):
      return bool(self.cont_type)

   # always called on finalized containers
   def add_to_container(self, cc, key, value):
      if self.cont_type != 'l':
         if self.additem is None:
            raise ConfigTypeError('container "%s" is immutable' % (key,))
         else:
            getattr(cc[key], self.additem)(value)
      else:
         cc[key].append(value)

   def finalize_container(self, cc, key):
      if self.cont_type != 'l':
         OrderedDict.__setitem__(cc, key, self.constructor(cc.is_pending[key]))
      else:
         OrderedDict.__setitem__(cc, key, cc.is_pending[key])

      del cc.is_pending[key]

def get_helper(s):
   return TypeHelper(s)

def is_container(s):
   """True if type is a container.
   ConfigTypeError is raised if the type is not recognized."""
   if s == '_child':
      return False

   return get_helper(s).is_container()

def has_type(s):
   """Checks that the container (if present) and item components are both recognized.
   Raises ConfigTypeError if argument isn't a string."""
   if not isinstance(s, basestring):
      raise ConfigTypeError('type must be a string')

   try:
      get_helper(s)

   except ConfigTypeError:
      return False

   else:
      return True

def validate(value, whatis):
   if whatis is None:
      return value
   else:
      return types[whatis](value)


__all__ = ('has_type', 'add_type', 'get_type', 'is_container', 'has_container', 'add_container')
