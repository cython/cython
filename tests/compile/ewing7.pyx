# mode: compile

cdef class A:
    cdef void f(self, x):
        pass

cdef class B(A):
    cdef void f(self, object x):
        pass

cdef extern void g(A a, b)

cdef extern void g(A a, b)

