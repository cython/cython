__doc__ = u"""
  >>> try:
  ...     B()
  ... except Exception, e:
  ...     print("%s: %s" % (e.__class__.__name__, e))
  Exception: crash-me
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"Exception, e", u"Exception as e")

cdef class A:
    def __cinit__(self):
        raise Exception(u"crash-me")

cdef class B(A):
    def __cinit__(self):
        print "hello world"
