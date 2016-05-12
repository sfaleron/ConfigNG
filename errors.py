
class ConfigBaseError(Exception):
   pass

class ConfigKeyError(ConfigBaseError, KeyError):
   pass

class ConfigTypeError(ConfigBaseError, TypeError):
   pass

class ConfigValueError(ConfigBaseError, ValueError):
   pass

class ConfigIncompleteError(Exception):
   pass
