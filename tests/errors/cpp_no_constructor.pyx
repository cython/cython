cdef extern from *:
    cdef cppclass Foo:
        Foo()
        Foo(int)

new Foo(1, 2)

_ERRORS = u"""
6:7: no suitable method found
"""
