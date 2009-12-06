__doc__ = u"""
    >>> D = set_longlong(2**40, 2**50, 2, "yelp")
    >>> D[2**40]
    'yelp'
    >>> D[2**50]
    'yelp'
    >>> D[2]
    'yelp'
"""

ctypedef long long foo

def set_longlong(long long ob, foo x, long y, val):
    cdef object tank = {}
    tank[ob] = val
    tank[x] = val
    tank[y] = val
    return tank
