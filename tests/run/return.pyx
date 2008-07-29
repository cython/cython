__doc__ = u"""
    >>> f('test')
    >>> test_g()
    >>> test_h(5)
    5
"""

def f(a):
    return
    return a
    return 42

cdef void g():
    return

cdef int h(a):
    cdef int i
    i = a
    return i

def test_g():
    g()

def test_h(i):
    return h(i)
