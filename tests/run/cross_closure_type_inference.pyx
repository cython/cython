# mode: run
# tag: typeinference

cimport cython


def test_outer_inner_double():
    """
    >>> print(test_outer_inner_double())
    double
    """
    x = 1.0
    def inner():
        nonlocal x
        x = 2.0
    inner()
    assert x == 2.0, str(x)
    return cython.typeof(x)


def test_outer_inner_double_int():
    """
    >>> print(test_outer_inner_double_int())
    ('double', 'double')
    """
    x = 1.0
    y = 2
    def inner():
        nonlocal x, y
        x = 1
        y = 2.0
    inner()
    return cython.typeof(x), cython.typeof(y)


def test_outer_inner_pyarg():
    """
    >>> print(test_outer_inner_pyarg())
    2
    long
    """
    x = 1
    def inner(y):
        return x + y
    print inner(1)
    return cython.typeof(x)


def test_outer_inner_carg():
    """
    >>> print(test_outer_inner_carg())
    2.0
    long
    """
    x = 1
    def inner(double y):
        return x + y
    print inner(1)
    return cython.typeof(x)


def test_outer_inner_incompatible():
    """
    >>> print(test_outer_inner_incompatible())
    Python object
    """
    x = 1.0
    def inner():
        nonlocal x
        x = 'test'
    inner()
    return cython.typeof(x)


def test_outer_inner_ptr():
    """
    >>> print(test_outer_inner_ptr())
    double *
    """
    x = 1.0
    xptr_outer = &x
    def inner():
        nonlocal x
        x = 1
        xptr_inner = &x
        assert cython.typeof(xptr_inner) == cython.typeof(xptr_outer), (
            '%s != %s' % (cython.typeof(xptr_inner), cython.typeof(xptr_outer)))
    inner()
    return cython.typeof(xptr_outer)


def test_outer_inner2_double():
    """
    >>> print(test_outer_inner2_double())
    double
    """
    x = 1.0
    def inner1():
        nonlocal x
        x = 2
    def inner2():
        nonlocal x
        x = 3.0
    inner1()
    inner2()
    return cython.typeof(x)
