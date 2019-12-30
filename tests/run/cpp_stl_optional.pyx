# ticket: 3293
# mode: run
# tag: cpp, werror
# distutils: extra_compile_args=-std=c++17

from cython.operator cimport dereference as deref
from libcpp.optional cimport optional
from libcpp cimport bool

def simple_test():
    """
    >>> simple_test()
    """
    cdef optional[int] o
    
    assert(not o.has_value())
    o = 5
    assert(o.has_value())
    assert(o.value()==5)
    o.reset()
    assert(not o.has_value())

