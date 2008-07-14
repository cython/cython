cdef int f() except -1:
    cdef type t1, t2
    cdef object x
    cdef int b
    b = typecheck(x, t1)
    b = issubtype(t1, t2)
