# mode: run

cdef class A:
    pass

cdef class B(A):
    pass

cdef class Foo:
    @staticmethod
    cdef A meth():
        return A()


cdef class Bar(Foo):
    @staticmethod
    cdef B meth():
        return B()

