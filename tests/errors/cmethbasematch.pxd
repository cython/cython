cdef class Base(object):
  cdef f(self)

cdef class MissingRedeclaration(Base):
  pass

cdef class BadRedeclaration(Base):
  cdef f(self)

cdef class NarrowerReturn(Base):
  pass
