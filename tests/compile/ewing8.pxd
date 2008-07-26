cdef struct Foo
cdef class Blarg

ctypedef Foo FooType
ctypedef Blarg BlargType

cdef struct Foo:
	FooType *f

cdef class Blarg:
	cdef FooType *f
	cdef BlargType b
