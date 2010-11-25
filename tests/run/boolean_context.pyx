
def test():
    """
    >>> test()
    True
    """
    cdef int x = 5
    return bool(x)

def test_bool_and_int():
    """
    >>> test_bool_and_int()
    1
    """
    cdef int x = 5
    cdef int b = bool(x)
    return b
