# ticket: t429

__doc__ = u"""
>>> sorted( get_locals(1,2,3, k=5) .items())
[('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]

"""

def get_locals(x, *args, **kwds):
    cdef int z = 5
    y = "hi"
    return locals()

def get_locals_rebound(x, *args, **kwds):
    """
    >>> get_locals_rebound(1,2,3)
    'REBOUND'
    """
    cdef int z = 5
    locals = _locals
    y = "hi"
    return locals()

def _locals(): return "REBOUND"

def sorted(it):
    l = list(it)
    l.sort()
    return l
