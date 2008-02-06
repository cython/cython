__doc__ = """
    >>> unpack_normal([1,2])
    (1, 2)
    >>> unpack_normal([1,2,3])
    Traceback (most recent call last):
    ValueError: too many values to unpack

    >>> unpack_comp([1,2])
    (1, 2)
    >>> unpack_comp([1,2,3])
    Traceback (most recent call last):
    ValueError: too many values to unpack

    >>> unpack_expr([1,2])
    (1, 2)
    >>> unpack_expr([1,2,3])
    Traceback (most recent call last):
    ValueError: too many values to unpack
"""

def unpack_normal(l):
    a,b = l
    return a,b

def unpack_comp(l):
    a,b = [ n for n in l ]
    return a,b

def unpack_expr(l):
    a,b = [ n*n for n in l ]
    return a,b
