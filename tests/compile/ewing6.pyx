# mode: compile
# Spurious gcc3.3 warnings about incompatible pointer
# types passed to C method

# Ordering of declarations in C code is important
cdef class C
cdef class D(C)
cdef class E

cdef class C:
    cdef void a(self):
        pass

cdef class D(C):
    cdef void m(self, E e):
        pass

cdef class E:
    pass

cdef void f(D d, E e):
    d.m(e)

f(D(),E())
