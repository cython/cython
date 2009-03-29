cdef extern from *:
    ctypedef class __builtin__.list [object PyListObject]:
        pass

cdef list foo = []

# This is too invasive for Python 0.11.x, re-enable in 0.12
NEW_ERRORS = u"""
:2:4: list already a builtin Cython type
"""

_ERRORS = u"""
5:16: Cannot coerce list to type 'list'
"""

