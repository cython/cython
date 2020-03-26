# mode: error

cdef class C:
    cdef void f(self):
        pass

cdef class D(C):
    cdef void f(self, int x):
        pass

# These are declared in the pxd.
cdef class Base(object):
  cdef f(self):
    pass

cdef class MissingRedeclaration(Base):
  # Not declared (so assumed cdef) in the pxd.
  cpdef f(self):
    pass

cdef class BadRedeclaration(Base):
  # Declared as cdef in the pxd.
  cpdef f(self):
    pass

cdef class UnneededRedeclaration(Base):
  # This is OK, as it's not declared in the pxd.
  cpdef f(self):
    pass

cdef class NarrowerReturn(Base):
  # This does not require a new vtable entry.
  cdef Base f(self):
    pass


_ERRORS = u"""
8: 9: Signature not compatible with previous declaration
4: 9: Previous declaration is here
# TODO(robertwb): Re-enable these errors.
#18:8: Compatible but non-identical C method 'f' not redeclared in definition part of extension type 'MissingRedeclaration'
#2:9: Previous declaration is here
#23:8: Compatible but non-identical C method 'f' not redeclared in definition part of extension type 'BadRedeclaration'
#2:9: Previous declaration is here
"""
