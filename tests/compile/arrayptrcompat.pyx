cdef enum E:
    z

cdef void f():
    cdef int *p
    cdef void *v
    cdef int a[5]
    cdef int i
    cdef E e
    p = a
    v = a
    p = a + i
    p = a + e
    p = i + a
    p = e + a
    p = a - i
    p = a - e
