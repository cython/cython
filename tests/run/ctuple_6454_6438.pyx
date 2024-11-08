# mode: run

ctypedef unsigned short i

cdef struct s:
    int x
    unsigned long y
    char z

ctypedef (int, int, s) v
ctypedef (long, long, s) z

ctypedef (void*, i, void*, v, z, z*) c

ctypedef fused a:
    v
    z

cdef v test(a p):
    return p

"""assert test((NULL, 5, NULL, (1, 2, s(5, 4, 3)), (11, 22, s(55, 44, 33)), NULL)) is False
assert test((NULL, 5, NULL, (1, 2, s(1, 4, 3)), (11, 22, s(55, 44, 33)), NULL)) is True
assert test((NULL, 5, NULL, (0, 2, s(5, 4, 3)), (11, 22, s(55, 44, 33)), NULL)) is True
assert test((NULL, 5, NULL, (11, 22, s(55, 44, 33)), (1, 2, s(5, 4, 3)), NULL)) is False
"""

print(test((1, 2, s(5, 4, 3))))