# mode: compile

cdef struct S:
    int q

def test():
    cdef int i = 1, j = 2, k = 3
    cdef float x = 1, y = 2, z = 3
    cdef object a = 1, b = 2, c = 3, d = 4, e = 5
    cdef int[3] m
    m[0] = 0
    m[1] = 1
    m[2] = 1
    cdef S s = [1]

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
