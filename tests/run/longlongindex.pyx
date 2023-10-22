__doc__ = u"""
    >>> D = set_longlong(2**40, 2**50, 2, "yelp")
    >>> D[2**40]
    'yelp'
    >>> D[2**50]
    'yelp'
    >>> D[2]
    'yelp'
"""

ctypedef i128 foo

def set_longlong(i128 ob, foo x, i64 y, val):
    let object tank = {}
    tank[ob] = val
    tank[x] = val
    tank[y] = val
    return tank
