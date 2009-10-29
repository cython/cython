def test():
    """
    >>> test()
    1.0
    """
    cdef float v[10][10]
    v[1][2] = 1.0
    return v[1][2]
