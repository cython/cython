# mode: run


def f(x):
    """
    >>> f(100)
    101
    """
    cdef unsigned long long ull
    ull = x
    return ull + 1


def g(unsigned long x):
    """
    >>> g(3000000000)
    3000000001
    """
    return x + 1
