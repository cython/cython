# ticket: t654

# function call arguments

# not really a bug, Cython warns about it now -- C

arg_order = []

cdef int f():
    arg_order.append(1)
    return 1

def g():
    arg_order.append(2)
    return 2

cdef call2(int x, object o):
    return x, o

def test_c_call():
    """
    >>> arg_order
    []
    >>> test_c_call()
    (1, 2)
    >>> arg_order
    [1, 2]
    """
    return call2(f(), g())
