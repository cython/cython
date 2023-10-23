# mode: compile

cdef class A:
    fn void f(self, x):
        pass

cdef class B(A):
    fn void f(self, object x):
        pass

cdef extern void g(A a, b)

cdef extern void g(A a, b)

