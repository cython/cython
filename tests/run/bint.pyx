from cython cimport typeof

def test(bint value):
    """
    >>> test(True)
    True
    >>> test(False)
    False
    >>> test(None)
    False

    >>> test(0)
    False
    >>> test(1)
    True
    >>> test(-1)
    True
    >>> test(100)
    True

    >>> test(0.0)
    False
    >>> test(0.1)
    True

    >>> test([])
    False
    >>> test([1, 2, 3])
    True
    """
    return value

def test_types(bint a):
    """
    >>> test_types(None)
    """
    cdef bint b = a
    assert typeof(a) == 'bint', typeof(a)
    assert typeof(b) == 'bint', typeof(b)
    c = b
    assert typeof(c) == 'bint', typeof(c)
