
"""Direct access is not intended; instead use the toplevel package."""

from __future__ import absolute_import
from __future__ import print_function

from .errors import *

from .configcont import ConfigCont

from minisup import do_string

import os.path as osp

import re

# detects a declaration or assignment
item_r = re.compile('([^:+=\\s][^:+=]*)(:|[+]?=)(.*)')

# detects a command
cmd_r  = re.compile('%([\\S]*)\\s+(.*)')


try:
   import localsettings as ls
   global_cfg = ls.get_global_cfg()

except ImportError:
   global_cfg = ''

class ConfigParserError(Exception):
   def __init__(self, *args):
      e, n, fn = args
      self.args = ('%s:%d:%s' % (fn, n, e),)

class ConfigIOError(ConfigBaseError):
   pass

def add_sign(f, sign):
   bits = osp.splitext(f)
   return '%s_%s%s' % ( bits[0], sign, bits[1] )

def findfile(f, dirs):
   dirs = list(dirs)
   if global_cfg:
      dirs.append(global_cfg)

   for i in dirs:
      path = osp.join(i, f)

      if osp.exists( path ):
         print(osp.normpath(path))
         return path

   print(dirs)
   raise ConfigIOError('File "%s" not found in include directories!' % (f,))

# python can be a little weird about nonscalar default function parameters
class ClearContext(dict):
   def __init__(self, fname):
      dict.__init__( self, { \
         'config'  : ConfigCont(None),
         'incdirs' : ['.'],
         'fname'   : fname,
         'n'       :     0 }
      )

def get_config(file_):
   """Takes a filename or stream; returns a configuraton container.
   Raises ConfigParserError if a descendent of ConfigBaseError is raised while processing."""
   return config_recursable(file_, **ClearContext(file_))

def config_recursable(file_, config, incdirs, fname='stream', n=0):

   if type(file_) == type(''):
      fd = open( findfile(file_, incdirs), 'r' )
      fname = file_
   else:
      fd = file_

   conts = []

   while True:
      ln = fd.readline()

      # end of file
      if not ln:
         break

      ln = ln.strip()

      # end of block
      if ln == '}':
         break

      n += 1

      if not ln:
         continue

      if ln.startswith('#'):
         continue

      try:
         m = cmd_r.match(ln)

         if m:
            # commands
            cmd, args  = m.groups()

            if   cmd == 'include':
               config_recursable(args, config, incdirs)

            elif cmd == 'dict' or cmd == 'odict':
               if args.endswith('{'):
                  key = args[:-1].strip()
                  d = config_recursable(     fd, ConfigCont(config), incdirs, fname, n )
               else:
                  idx = args.find('=')

                  if idx == -1:
                     raise ConfigParserError('Syntax Error', n, fname)

                  key = args[:idx].strip()
                  d   = config_recursable( args[idx+1:].strip(), ConfigCont(config), incdirs )

               config.add_child(key, d)

            elif cmd == 'includedir':
               incdirs.append(args)

            else:
               raise ConfigParserError('Unrecognized command', n, fname)

         else:
            # declarations and definitions
            m = item_r.match(ln)

            if not m:
               raise ConfigParserError('Syntax Error', n, fname)

            a, op, b = [i.strip() for i in m.groups()]

            if op == ':':
               key, whatis = a, b

               if not has_type(whatis):
                  raise ConfigParserError('Unsupported type "%s"' % (whatis,), n, fname)

               try:
                  if is_container(whatis):
                     config.add_container(key, whatis)
                     conts.append(key)
                  else:
                     config.add_item(key, whatis)

               except ConfigTypeError as e:
                  raise ConfigParserError('Unrecognized type "%s"' % (whatis,), n, fname)

            else:
               key, val = a, b

               if not config.has_key(key):
                  raise ConfigParserError('Unrecognized key "%s"' % (key,), n, fname)

               val, inc = do_string(fd, val)
               n += inc

               if op == '=':
                  config[key] = val

               else:
                  config.add_to_container(key, val)

      except ConfigBaseError as e:
         raise ConfigParserError(e[0], n, fname)

   if file_ is not fd:
      fd.close()

   for cont in conts:
      config.finalize_container(cont)

   return config

__all__ = ('get_config', 'ConfigParserError')

# cyclical imports, so it goes at the end
from .api import *
