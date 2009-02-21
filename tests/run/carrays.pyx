__doc__ = u"""
>>> test1()
2
>>> test2()
0
>>> test3()
(2, 3)
"""

def test1():
    cdef int x[2][2]
    x[0][0] = 1
    x[0][1] = 2
    x[1][0] = 3
    x[1][1] = 4
    return f(x)[1]

cdef int* f(int x[2][2]):
    return x[0]


def test2():
    cdef int a1[5]
    cdef int a2[2+3]
    return sizeof(a1) - sizeof(a2)

cdef enum:
    MY_SIZE_A = 2
    MY_SIZE_B = 3

def test3():
    cdef int a[MY_SIZE_A]
    cdef int b[MY_SIZE_B]
    return sizeof(a)/sizeof(int), sizeof(b)/sizeof(int)
