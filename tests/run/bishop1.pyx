cdef class fmatrix:
  cdef int foo

  def __setitem__(self, int key, int value):
    if key:
      self.foo = value
      return
    self.foo = not value
