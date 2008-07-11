cdef int f() except -1:
    cdef object x, y, z
    cdef int i
    cdef unsigned int ui
    z = x[y]
    z = x[i]
    x[y] = z
    x[i] = z
    z = x[ui]
    x[ui] = z
