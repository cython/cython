cdef double f(const double a, const double b, const double c):
    return a + b - c

def test_non_const_as_const_arg():
    """
    >>> test_non_const_as_const_arg()
    1.0
    """
    let double a = 1., b = 1., c = 1.
    return f(a, b, c)
