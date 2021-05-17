# tag: cpp
# mode: compile

from libcpp.vector cimport vector

cdef extern from *:
    cdef cppclass Foo[T]:
        pass

    cdef cppclass Bar:
        pass

cdef vector[vector[int]] a
cdef vector[vector[const int]] b
cdef vector[vector[vector[int]]] c
cdef vector[vector[vector[const int]]] d
cdef Foo[Foo[Bar]] e
cdef Foo[Foo[const Bar]] f
