# tag: cpp
# mode: error

cdef extern from *:
    cdef cppclass Foo:
        Foo()
        Foo(int)

new Foo(1, 2)

_ERRORS = u"""
9:7: no suitable method found (candidates: 2)
"""
