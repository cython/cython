# ticket: t245

cimport crashT245_pxd

def f():
    """
    >>> f()
    {'x': 1}
    """
    cdef crashT245_pxd.MyStruct s
    s.x = 1
    print s
