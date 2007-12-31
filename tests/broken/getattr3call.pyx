cdef int f(a, b, c) except -1:
    d = getattr3(a, b, c)
