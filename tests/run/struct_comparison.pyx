# mode: run

cdef struct b:
    unsigned char m1
    unsigned int m2

cdef struct a:
    int m1
    float m2
    b m3
    b *m4

cdef b b1 = b(-1, -2)

cdef a a1 = a(1, 2, b(3, 4), &b1)
cdef a a2 = a(3, 4, b(5, 6), &b1)

assert (a1 == a1) is True
assert (a1 == a2) is False
assert (a1 != a1) is False
assert (a1 != a2) is True
