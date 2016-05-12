
"""Validator factories"""

from errors import ConfigTypeError, ConfigValueError

from validators import validate_integer

class Range(object):
   """Accepts integers between two values, inclusively.
   Numbers may be equal and order is not significant."""
   def __init__(self, name, desc, n1, n2):

      self.__doc__ = desc

      if not isinstance(n1, (int, long)) or not isinstance(n2, (int, long)):
         raise ConfigTypeError('integers are required')

      if n2 < n1:
         n1, n2 = n2, n1

      self.min_ = n1
      self.max_ = n2

      self.errmsg = '%s value must be within %d and %d, inclusively' % (name, n1, n2)

   def __call__(self, s):
      n = validate_integer(s)

      if self.min_ <= n <= self.max_:
         return n
      else:
         raise ConfigValueError(self.errmsg)

from collections import Iterable, Hashable

class Choice(object):
   """Select from a list of predetermined strings (or other hashable).
   Raises ConfigTypeError if the iterable of strings (or other hasables) isn't."""
   def __init__(self, name, choices):

      if not isinstance(choices, Iterable):
         raise ConfigTypeError('finite, nonempty iterable of strings (or other hasables) required')

      for i in choices:
         if not isinstance(i, Hashable):
            raise ConfigTypeError('finite, nonempty iterable of strings (or other hasables) required')

      self.choices = choices = tuple(choices)

      if   len(choices) == 0:
            raise ConfigTypeError('finite, nonempty iterable of strings (or other hasables) required')
      elif len(choices) == 1:
         choicemsg = '"%s"' % (choices[0],)
      elif len(choices) == 2:
         choicemsg = '"%s" or "%s"' % choices
      else:
         choicemsg = ', '.join(['"%s"' % (i,) for i in choices[:-1]]) + ', or "%s"' % choices[-1:]

      self.errmsg = '%s value must be %s.' % (name, choicemsg)

      self.__doc__ = '%s; valid choices are: %s.' % (name, choicemsg)

   def __call__(self, s):
      if not isinstance(s, Hashable):
         raise ConfigTypeError(self.errmsg)

      if s in self.choices:
         return s
      else:
         raise ConfigValueError(self.errmsg)

import sys

from collections import Sequence

class PlatformMixer(object):
   """Choice of values, depending on whether the platform isn't windows, or is."""
   def __init__(self, longdesc, plural, validator):
      self.mixedthing =   plural
      self.validator = validator
      self.__doc__  = \
   """%s, chosen from a pair, depending on platform.
   Takes two newline delimited %s and returns the first when
   not run under windows, otherwise returns the second.""" % (longdesc, plural)

   def __call__(self, s):
      if not isinstance(s, basestring):
         if isinstance(s, Sequence):
            l = s
         else:
            raise ConfigValueError('requires two newline delimited %s (string), or a length-two sequence' % (self.mixedthing,))
      else:
         l = s.strip().splitlines()

      if len(l) != 2:
         raise ConfigValueError('requires two newline delimited %s (string), or a length-two sequence' % (self.mixedthing,))
      else:
         return self.validator(l[int(sys.platform == 'win32')])

from types import get_type, add_type

__all__ = ('Range', 'Choice', 'PlatformMixer', 'get_type', 'add_type')
