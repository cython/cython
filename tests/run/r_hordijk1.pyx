__doc__ = """
  >>> try:
  ...     s = Spam()
  ... except KeyError, e:
  ...     print("Exception: %s" % e)
  ... else:
  ...     print("Did not raise the expected exception")
  Exception: 'This is not a spanish inquisition'
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace("Error, e", "Error as e")

cdef extern from "Python.h":
    ctypedef class __builtin__.list [object PyListObject]:
        pass

cdef class Spam(list):
    def __init__(self):
        raise KeyError("This is not a spanish inquisition")
