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

  def __setitem__(self, int key, int value):
    if key:
      self.foo = value
      return
    self.foo = not value

  def getfoo(self):
    return self.foo
