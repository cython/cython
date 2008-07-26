cdef class C:
    cdef int i

cdef int f() except -1:
    cdef object x
    cdef void *p
    cdef int i
    x = <object>p
    p = <void *>x
    x = (<object>p).foo
    i = (<C>p).i
    (<C>p).i = i
