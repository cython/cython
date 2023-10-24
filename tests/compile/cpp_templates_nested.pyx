# tag: cpp
# mode: compile

from libcpp.vector cimport vector

extern from *:
    cdef cppclass Foo[T]:
        pass

    cdef cppclass Bar:
        pass

cdef vector[vector[i32]] a
cdef vector[vector[const i32]] b
cdef vector[vector[vector[i32]]] c
cdef vector[vector[vector[const i32]]] d
cdef Foo[Foo[Bar]] e
cdef Foo[Foo[const Bar]] f
