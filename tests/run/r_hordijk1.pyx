__doc__ = u"""
  >>> try:
  ...     s = Spam()
  ... except KeyError, e:
  ...     print("Exception: %s" % e)
  ... else:
  ...     print("Did not raise the expected exception")
  Exception: u'This is not a spanish inquisition'
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"Error, e", u"Error as e")
    __doc__ = __doc__.replace(u" u'", u" '")

cdef extern from "Python.h":
    ctypedef class __builtin__.list [object PyListObject]:
        pass

cdef class Spam(list):
    def __init__(self):
        raise KeyError(u"This is not a spanish inquisition")
