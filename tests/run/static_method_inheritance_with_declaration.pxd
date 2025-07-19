cdef class A:
    pass

cdef class B(A):
    pass

cdef class GetBaseA:
    @staticmethod
    cdef A meth()

cdef class GetSubB(GetBaseA):
    @staticmethod
    cdef B meth()

