# ticket: t430

__doc__ = u"""
>>> sorted( get_locals(1,2,3, k=5) .items())
[('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]

>>> sorted(get_locals_items(1,2,3, k=5))
[('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]

>>> sorted(get_locals_items_listcomp(1,2,3, k=5))
[('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]
"""

def get_locals(x, *args, **kwds):
    cdef int z = 5
    y = "hi"
    return locals()

def get_locals_items(x, *args, **kwds):
    cdef int z = 5
    y = "hi"
    return locals().items()

def get_locals_items_listcomp(x, *args, **kwds):
    # FIXME: 'item' should *not* appear in locals() yet, as locals()
    # is evaluated before assigning to item !
    cdef int z = 5
    y = "hi"
    return [ item for item in locals().items() ]

def sorted(it):
    l = list(it)
    l.sort()
    return l
