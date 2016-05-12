
from types import *
from types import validate, get_helper

from errors import *

from collections import OrderedDict


class ConfigCont(OrderedDict):
   def __init__(self, parent=None):
      self.whatis = {}
      self.is_pending = {}
      self.set_parent(parent)

      OrderedDict.__init__(self)

   def add_child(self, key, cc):
      """Adds a subsection to the configuration.
      Raises ConfigTypeError if object is not a ConfigCont,
      and ConfigKeyError if the key is in use."""
      if not isinstance(cc, ConfigCont):
         raise ConfigTypeError('not a configuration container')

      if key in self.whatis:
         raise ConfigKeyError('cannot overwrite existing element ' + key)

      self.whatis[key] = '_child'
      OrderedDict.__setitem__(self, key, cc)

   def has_key(self, key):
      """True if the element is declared, whether or not it's been defined"""
      return key in self.whatis

   # element must be declared
   def _add_to_or_set_element(self, key, valin, cont_expected):
      if self.has_key(key):
         helper = get_helper(self.whatis[key])

         valout = validate(valin, helper.item_type)

         if helper.is_container():
            if not cont_expected:
               raise ConfigKeyError('cannot overwrite existing container')

            if key in self:
               helper.add_to_container(self, key, valout)
            else:
               self.is_pending[key].append(valout)
         else:
            if cont_expected:
               raise ConfigKeyError('configuration element is not a container')

            OrderedDict.__setitem__(self, key, valout)

      else:
         raise ConfigKeyError('configuration element is not declared')

   def __setitem__(self, key, value):
      """Item must be be declared. ConfigKeyError is raised if it isn't, it's a container,
      or it's a configuration container. ConfigValueError is raised if validation fails."""
      if not self.has_key(key):
         raise ConfigKeyError('configuration element is not declared')

      if self.whatis[key] == '_child':
         raise ConfigKeyError('cannot overwrite existing configuation container ' + key)

      self._add_to_or_set_element(key, value, False)

   def add_to_container(self, key, value):
      """Container must be be declared. ConfigKeyError is raised if it isn't, or it isn't a container.
      ConfigValueError is raised if validation fails."""

      self._add_to_or_set_element(key, value, True)

   def add_container(self, key, whatis):
      """Declare and define a new container. Raises ConfigKeyError if key is in use,
      ConfigTypeError if it isn't a container type."""

      if key in self.whatis:
         raise ConfigKeyError('cannot overwrite existing container or item ' + key)

      if not is_container(whatis):
         raise ConfigTypeError('type %s is not a container' % (whatis,))

      # start out as a list, convert to final type when its items are defined
      self.is_pending[key] = []
      self.whatis[key] = whatis

   def finalize_container(self, key):
      """Finalize a container; containers become their intended type. ConfigKeyError is
      raised if the key is not found among the pending containers."""
      if not key in self.is_pending:
         raise ConfigKeyError('pending container %s not found' % (key,))

      get_helper(self.whatis[key]).finalize_container(self, key)

   def add_item(self, key, whatis):
      """Declares a new item. Raises ConfigKeyError if key is in use,
      ConfigTypeError if it isn't an item type."""

      if key in self.whatis:
         raise ConfigKeyError('cannot overwrite existing container or item ' + key)

      if is_container(whatis):
         raise ConfigTypeError('%s is not an item' % (key,))

      self.whatis[key] = whatis

   def add_untyped(self, key, value):
      """Convenience method for expanding the configuration at runtime.
      Raises ConfigKeyError if key is in use."""

      if key in self.whatis:
         raise ConfigKeyError('cannot overwrite existing container or item ' + key)

      self.whatis[key] = None
      self[key] = value

   def set_parent(self, parent):
      """Supports pruning and grafting of configuration trees.
      Raises ConfigTypeError if object is not a ConfigCont or None."""
      if not (parent is None or isinstance(parent, ConfigCont)):
         raise ConfigTypeError('not a configuration container')

      self.parent = parent

   def check_completeness(self, path='root'):
      """Raises ConfigIncompleteError if any elements are not defined. Recurses into
      child containere."""
      s = set(self.whatis) - set(self)

      if s:
         raise ConfigIncompleteError('undefined elements remain: %s: %s' % (path, ','.join(s)))

      for k,v in self.iteritems():
         if self.whatis[k] == '_child':
            v.check_completeness('%s:%s' % (path, k))

__all__ = ('ConfigCont',)
