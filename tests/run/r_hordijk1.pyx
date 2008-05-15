__doc__ = u"""
  >>> try:
  ...     s = Spam()
  ... except StandardError, e:
  ...     print("Exception: %s" % e)
  ... else:
  ...     print("Did not raise the expected exception")
  Exception: This is not a spanish inquisition
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"Exception, e", u"Exception as e")

cdef extern from "Python.h":
    ctypedef class types.ListType [object PyListObject]:
        pass

cdef class Spam(ListType):
    def __init__(self):
        raise StandardError("This is not a spanish inquisition")
