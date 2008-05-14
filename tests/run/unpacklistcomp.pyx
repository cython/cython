__doc__ = u"""
    >>> unpack_normal([1,2])
    (1, 2)
    >>> unpack_normal([1,2,3]) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...

    >>> unpack_comp([1,2])
    (1, 2)
    >>> unpack_comp([1,2,3]) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...

    >>> unpack_expr([1,2])
    (1, 4)
    >>> unpack_expr([1,2,3]) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
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
