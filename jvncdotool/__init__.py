# https://twistedmatrix.com/trac/ticket/3413#comment:21
# workaround for Jython, see: http://bugs.jython.org/issue1521
import __builtin__
if not hasattr(__builtin__, 'buffer'):
    def _buffer(object, offset = None, size = None):
       if offset is None:
          offset = 0
       if size is None:
          size = len(object)
       return object[offset:offset+size]
    __builtin__.buffer = _buffer

import twisted.python.deprecate
twisted.python.deprecate.deprecatedModuleAttribute=lambda *x: None

import types
import twisted.python.runtime
del twisted.python.runtime.Platform.isWindows
twisted.python.runtime.Platform.isWindows = types.MethodType(lambda x: __import__("java.lang.System").lang.System.getProperty('os.name').lower().startswith('windows'), None, twisted.python.runtime.Platform)

import threading
setattr(threading.JavaThread, "ident", None)

threading.Thread.org_Thread__bootstrap = threading.Thread._Thread__bootstrap
del threading.Thread._Thread__bootstrap

def new__bootstrap(self):
    self.ident=__import__("random").randint(1, 1000)
    self.org_Thread__bootstrap()
threading.Thread._Thread__bootstrap = types.MethodType(new__bootstrap, None, threading.Thread)
