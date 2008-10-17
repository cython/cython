ctypedef struct Foo:
    int blarg

cdef Foo f():
    blarg = 1 + 2

f()
