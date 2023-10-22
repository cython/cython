def f(a):
    """
    >>> f('test')
    """
    return
    return a
    return 42

cdef void g():
    return

cdef int h(a):
    let int i
    i = a
    return i

cdef const int p():
    return 1

def test_g():
    """
    >>> test_g()
    """
    g()

def test_h(i):
    """
    >>> test_h(5)
    5
    """
    return h(i)

def test_p():
    """
    >>> test_p()
    1
    """
    return p()
