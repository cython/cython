# mode: error

cdef struct a:
    int m1
    int m2

print(a(1, 2) == a(3, 4))
