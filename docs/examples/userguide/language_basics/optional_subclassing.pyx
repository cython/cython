 
cdef class A:

    cdef foo(self):
        print("A")


cdef class B(A):

    cdef foo(self, x=None):
        print("B", x)


cdef class C(B):

    cpdef foo(self, x=True, int k=3):
        print("C", x, k)
