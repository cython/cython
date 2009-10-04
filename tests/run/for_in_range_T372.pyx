__doc__ = u"""
>>> test_modify()
0 1 2 3 4
(4, 0)
>>> test_fix()
0 1 2 3 4
4
>>> test_break()
0 1 2
(2, 0)
>>> test_return()
0 1 2
(2, 0)
"""

def test_modify():
    cdef int i, n = 5
    for i in range(n):
        print i,
        n = 0
    print
    return i,n

def test_fix():
    cdef int i
    for i in range(5):
        print i,
    print
    return i

def test_break():
    cdef int i, n = 5
    for i in range(n):
        print i,
        n = 0
        if i == 2:
            break
    print
    return i,n

def test_return():
    cdef int i, n = 5
    for i in range(n):
        print i,
        n = 0
        if i == 2:
            return i,n
    print
    return "FAILED!"
