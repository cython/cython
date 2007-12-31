__doc__ = """
  >>> try:
  ...     s = Spam()
  ... except StandardError, e:
  ...     print "Exception:", e
  ... else:
  ...     print "Did not raise the expected exception"
  Exception: This is not a spanish inquisition
"""

cdef extern from "Python.h":
    ctypedef class types.ListType [object PyListObject]:
        pass

cdef class Spam(ListType):
    def __init__(self):
        raise StandardError("This is not a spanish inquisition")
