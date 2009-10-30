def test():
    """
    >>> test() == 55 + 66
    True
    """
    cdef int a,b
    foo=(55,66)
    a,b=foo
    return a + b
