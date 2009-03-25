cdef extern from *:
    ctypedef class __builtin__.list [object PyListObject]:
        pass

cdef list foo = []
_ERRORS = u"""
:2:4: list already a builtin Cython type
"""
