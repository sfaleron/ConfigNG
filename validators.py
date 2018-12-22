
"""Direct access is not intended; instead use the api module."""

# validators return the parsed/converted value on success, and raises
# ConfigValueError otherwise.

from __future__ import absolute_import

from .errors import ConfigTypeError, ConfigValueError

from .types import add_type

try:
   basestring
except NameError:
   basestring = str

try:
    intTypes  = (int, long)
except NameError:
    intTypes  = int


def validate_string(s):
   """stringiness is obligatory"""
   if not isinstance(s, basestring):
      raise ConfigTypeError('not a string')

   return s

def no_validation(s):
   """anything goes"""
   return s

def validate_boolean(s):
   """value may be "true" or "false", evaluates to Python boolean values True and False"""

   if isinstance(s, bool):
      return s

   if s == 'true':
      return True

   if s == 'false':
      return False

   if isinstance(s, basestring):
      raise ConfigValueError('boolean value must be "true" or "false".')
   else:
      raise ConfigTypeError('boolean value must be "true" or "false".')


import re
notdigit_r = re.compile('[^0-9]')

def validate_integer(s):
   """digits and negative sign only. will not convert a decimal value!"""

   if isinstance(s, intTypes):
      return s

   if not isinstance(s, basestring):
      raise ConfigTypeError('integer value may contain only digits and a leading negative sign')

   negate = s.startswith('-')
   if negate:
      s = s[1:]

   if notdigit_r.search(s):
      raise ConfigValueError('integer value may contain only digits and a leading negative sign')

   try:
      return (-1 if negate else 1) * int(s)

   except ValueError as e:
      raise ConfigValueError(e)


def validate_float(s):
   """passed straight into float() built-in function"""
   try:
      return float(s)

   except TypeError as e:
      raise ConfigTypeError(e)

   except ValueError as e:
      raise ConfigValueError(e)


import os.path as osp
import os, tempfile

# path validation checks for any exception. typeerror and ioerror are observed,
# but it isn't clear to me what may be expected in general.

def validate_path(s):
   """leading part of path must exist, and the last element be a valid directory
   entry. symbolic links are followed"""

   if not isinstance(s, basestring):
      raise ConfigTypeError('not a string')

   base, fn = osp.split(s)

   if base:
      try:
         if not osp.exists(base):
            raise ConfigValueError('directory not found')
      except:
         raise ConfigValueError('invalid directory')

   tmpd = tempfile.mkdtemp()

   try:
      tmpf = osp.join(tmpd, fn)
      open(tmpf, 'w').close()
      os.remove(tmpf)

   except:
      raise ConfigValueError('invalid filename')

   finally:
      os.rmdir(tmpd)

   return s


def validate_existing_path(s):
   """an existing directory entry (file, directory, or perhaps something else)."""
   validate_path(s)

   if not osp.exists(s):
      raise ConfigValueError('path not found')

   return s


def validate_existing_dir(s):
   """an existing directory."""
   validate_existing_path(s)

   if not osp.isdir(s):
      raise ConfigValueError('path is not a directory')

   return s


def validate_existing_file(s):
   """an existing file."""
   validate_existing_path(s)

   if not osp.isfile(s):
      raise ConfigValueError('path is not a file')

   return s


add_type('notype', no_validation)
add_type('str',    validate_string)
add_type('bool',   validate_boolean)
add_type('int',    validate_integer)
add_type('fp',     validate_float)

add_type('path',   validate_path)
add_type('epath',  validate_existing_path)
add_type('dir',    validate_existing_dir)
add_type('file',   validate_existing_file)

from .factories import *

add_type('userport', Range('user tcp/ip port', 'nonpriviledged port numbers, 1024-65535', 1024, 65535))

add_type('platmixd', PlatformMixer('an existing directory', 'directories', validate_existing_dir))
add_type('platmixf', PlatformMixer('an existing file',      'files',       validate_existing_file))
