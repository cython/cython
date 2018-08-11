from __future__ import print_function

cdef class A:
    cdef foo(self):
        print("A")

cdef class B(A):
    cpdef foo(self):
        print("B")

class C(B):  # NOTE: not cdef class
    def foo(self):
        print("C")
