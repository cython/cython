def test():
    """
    >>> test()
    1.0
    """
    cdef float[10][10] v
    v[1][2] = 1.0
    return v[1][2]
