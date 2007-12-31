__doc__ = """
  >>> try:
  ...     B()
  ... except Exception, e:
  ...     print "%s: %s" % (e.__class__.__name__, e)
  Exception: crash-me
"""

cdef class A:
    def __cinit__(self):
        raise Exception("crash-me")

cdef class B(A):
    def __cinit__(self):
        print "hello world"
