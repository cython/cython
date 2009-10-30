__doc__ = u"""
>>> sorted( get_locals(1,2,3, k=5) .items())
[('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]

"""

def get_locals(x, *args, **kwds):
    cdef int z = 5
    y = "hi"
    return locals()

def in_locals(x, *args, **kwds):
    """
    >>> in_locals('z')
    True
    >>> in_locals('args')
    True
    >>> in_locals('X')
    False
    """
    cdef int z = 5
    y = "hi"
    return x in locals()

def sorted(it):
    l = list(it)
    l.sort()
    return l
