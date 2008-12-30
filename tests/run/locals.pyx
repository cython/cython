__doc__ = u"""
>>> sorted( get_locals(1,2,3, k=5) .items())
[('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]
"""

import sys
IS_PY3 = sys.version_info[0] >= 3

def get_locals(x, *args, **kwds):
    cdef int z = 5
    if IS_PY3:
        y = u"hi"
    else:
        y = "hi"
    return locals()

def sorted(it):
    l = list(it)
    l.sort()
    return l
