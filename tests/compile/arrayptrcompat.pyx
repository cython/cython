# mode: compile
# tag: test_in_limited_api

cdef enum E:
    z

cdef void f():
    cdef int *p
    cdef void *v
    cdef int[5] a
    cdef int i=0
    cdef E e=z
    p = a
    v = a
    p = a + i
    p = a + e
    p = i + a
    p = e + a
    p = a - i
    p = a - e

f()
