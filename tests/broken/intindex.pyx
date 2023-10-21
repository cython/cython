cdef int f() except -1:
    cdef object x, y, z
    cdef i32 i
    cdef u32 ui
    z = x[y]
    z = x[i]
    x[y] = z
    x[i] = z
    z = x[ui]
    x[ui] = z
