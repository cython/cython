# tag: cpp
# mode: error

extern from *:
    cdef cppclass Foo:
        Foo()
        Foo(i32)

new Foo(1, 2)

_ERRORS = u"""
9:7: Call with wrong number of arguments (expected 1, got 2)
"""
