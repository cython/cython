__doc__ = u"""
    >>> m = fmatrix()
    >>> m[1] = True
    >>> m.getfoo()
    1
    >>> m[0] = True
    >>> m.getfoo()
    0
"""

cdef class fmatrix:
  cdef int foo

  def __setitem__(self, i32 key, i32 value):
    if key:
      self.foo = value
      return
    self.foo = not value

  def getfoo(self):
    return self.foo
