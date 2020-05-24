# mode: error
# tag: no-cpp, werror

from cython.operator import typeid

def use_typeid():
    cdef int i = 0
    print typeid(i) == typeid(i)

_ERRORS = """
8:10: typeid operator only allowed in c++
8:23: typeid operator only allowed in c++
"""
