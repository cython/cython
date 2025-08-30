# tag: cpp
# mode: error

from libcpp.string cimport string

cdef foo():
    cdef string field
    if field:  # field cannot be coerced to bool
        pass

_ERRORS = u"""
8:7: Type 'string' not acceptable as a boolean
"""
