cdef int g = 7

def test(x, int y):
    """
    >>> test(1, 2)
    4 1 2 2 0 7 8
    """
    if True:
        before = 0
    cdef int a = 4, b = x, c = y
    cdef int *p = &y
    cdef object o = int(8)
    print a, b, c, p[0], before, g, o

# Also test that pruning cdefs doesn't hurt
def empty():
    cdef int i
