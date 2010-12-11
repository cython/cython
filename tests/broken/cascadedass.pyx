cdef void foo():
    cdef int i, j, k
    i = j = k
    a = b = c
    i = j = c
    a = b = k
    (a, b), c = (d, e), f = (x, y), z
#	a, b = p, q = x, y
