def test(x):
    """
    >>> test(3)
    3
    """
    return retinput(x)

cdef inline int retinput(int x):
    o = x
    return o
