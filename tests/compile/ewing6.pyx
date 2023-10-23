# mode: compile
# Spurious gcc3.3 warnings about incompatible pointer
# types passed to C method

# Ordering of declarations in C code is important
cdef class C
cdef class D(C)
cdef class E

cdef class C:
    fn void a(self):
        pass

cdef class D(C):
    fn void m(self, E e):
        pass

cdef class E:
    pass

fn void f(D d, E e):
    d.m(e)

f(D(),E())
