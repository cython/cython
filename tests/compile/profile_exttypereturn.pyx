# mode: compile
# cython: profile=True

cdef class Foo:
    ...

cdef Foo _foo():
    return Foo()

def foo():
    return _foo()

