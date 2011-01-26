
order = []

cdef int f():
    order.append(1)
    return 1

def g():
    order.append(2)
    return 2

cdef call(int x, object o):
    return x, o

def test():
    """
    >>> order
    []
    >>> test()
    (1, 2)
    >>> order
    [1, 2]
    """
    return call(f(), g())
