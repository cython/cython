struct Foo
cdef class Blarg

ctypedef Foo FooType
ctypedef Blarg BlargType

struct Foo:
    FooType *f

cdef class Blarg:
    cdef FooType *f
    cdef BlargType b
