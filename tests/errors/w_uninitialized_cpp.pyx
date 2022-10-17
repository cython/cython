# cython: warn.maybe_uninitialized=True
# mode: error
# tag: cpp, werror

from cython.operator import typeid

def uninitialized_in_typeid():
    cdef int i
    print typeid(i) == typeid(i)

_ERRORS = """
"""
