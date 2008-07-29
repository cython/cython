cdef struct S:
    int q

cdef int f() except -1:
    cdef int i, j, k
    cdef float x, y, z
    cdef object a, b, c, d, e
    cdef int m[3]
    cdef S s
    global g
    i += j + k
    x += y + z
    x += i
    a += b + c
    g += a
    m[i] += j
    a[i] += b + c
    a[b + c] += d
    (a + b)[c] += d
    a[i : j] += b
    (a + b)[i : j] += c
    a.b += c + d
    (a + b).c += d
    s.q += i
