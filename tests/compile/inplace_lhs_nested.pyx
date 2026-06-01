# mode: compile

cdef class A:
    cdef int b

cdef class C:
    cdef A _a


cdef void set_a(A a) noexcept nogil:
    a.b |= 1

cdef void set_b(C c) noexcept nogil:
    c._a.b |= 1

cdef void set_c(C c) noexcept nogil:
    c._a.b = c._a.b | 1
