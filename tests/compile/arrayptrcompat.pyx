# mode: compile

cdef enum E:
    Z

cdef void f():
    cdef i32 *p
    cdef void *v
    cdef i32[5] a
    cdef i32 i = 0
    cdef E e = Z
    p = a
    v = a
    p = a + i
    p = a + e
    p = i + a
    p = e + a
    p = a - i
    p = a - e

f()
