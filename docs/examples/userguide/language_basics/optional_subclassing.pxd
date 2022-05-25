cdef class A:
    cdef foo(self)

cdef class B(A):
    cdef foo(self, x=*)

cdef class C(B):
    cpdef foo(self, x=*, int k=*)
