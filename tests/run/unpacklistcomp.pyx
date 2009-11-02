def unpack_normal(l):
    """
    >>> unpack_normal([1,2])
    (1, 2)
    >>> unpack_normal([1,2,3]) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    """
    a,b = l
    return a,b

def unpack_comp(l):
    """
    >>> unpack_comp([1,2])
    (1, 2)
    >>> unpack_comp([1,2,3]) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    """
    a,b = [ n for n in l ]
    return a,b

def unpack_expr(l):
    """
    >>> unpack_expr([1,2])
    (1, 4)
    >>> unpack_expr([1,2,3]) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    """
    a,b = [ n*n for n in l ]
    return a,b
