# mode: error

ctypedef extern class xxx.C[object XXX, check_size opaque]:
    cdef int x  # not allowed with check_size=opaque

ctypedef extern class xxx.D[object XXX, check_size opaque]:
    pass

cdef class Derived(D):  # not allowed to inherit from an opaque type
    pass

_ERRORS = """
4:13: classes with check_size='opaque' cannot have declared members
9:19: Base class 'D' of type 'Derived' is opaque.
"""
