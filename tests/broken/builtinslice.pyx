cdef int f() except -1:
    cdef slice s
    cdef object z
    cdef int i
    z = slice
    s = slice(1, 2, 3)
    z = slice.indices()
    i = s.start
    i = s.stop
    i = s.step
