# mode: error
# tag: cpp

from libcpp.vector cimport vector

def f():
    cdef vector[int] v
    it = v.begin()
    while it != v.end():
        it = it * 2

_ERRORS = """
8:16: Cannot convert 'iterator' to Python object
9:13: Invalid types for '!=' (Python object, iterator)
"""
