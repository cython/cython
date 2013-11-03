t = (1,2,3)
l = [1,2,3]

def assign3(t):
    """
    >>> assign3(l)
    (1, 2, 3)
    >>> assign3(t)
    (1, 2, 3)
    >>> assign3((1,))
    Traceback (most recent call last):
    ValueError: need more than 1 value to unpack
    >>> assign3((1,2))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    >>> assign3((1,2,3,4))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)
    """
    a,b,c = t
    return (a,b,c)

def assign3_typed(tuple t):
    """
    >>> assign3_typed(t)
    (1, 2, 3)
    >>> assign3_typed(l)
    Traceback (most recent call last):
    TypeError: Argument 't' has incorrect type (expected tuple, got list)
    >>> a,b,c = (1,) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> assign3_typed((1,))
    Traceback (most recent call last):
    ValueError: need more than 1 value to unpack
    >>> a,b,c = (1,2) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> assign3_typed((1,2))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    >>> a,b,c = (1,2,3,4)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> assign3_typed((1,2,3,4))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)
    >>> a,b = 99,98
    >>> a,b = t     # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> a,b
    (99, 98)
    """
    a,b,c = t
    return (a,b,c)

def assign3_int(t):
    """
    >>> assign3_int(l)
    (1, 2, 3)
    """
    cdef int a,b,c
    a,b,c = t
    return (a,b,c)

def assign3_mixed1(t):
    """
    >>> assign3_mixed1(l)
    (1, 2, 3)
    """
    cdef int a
    a,b,c = t
    return (a,b,c)

def assign3_mixed2(t):
    """
    >>> assign3_mixed2(l)
    (1, 2, 3)
    """
    cdef int b
    a,b,c = t
    return (a,b,c)

def assign3_mixed3(t):
    """
    >>> assign3_mixed3(l)
    (1, 2, 3)
    """
    cdef int c
    a,b,c = t
    return (a,b,c)

def assign3_mixed4(t):
    cdef int b,c
    a,b,c = t
    return (a,b,c)

def test_overwrite(t):
    """
    >>> test_overwrite(l)
    (99, 98)
    >>> test_overwrite(t)
    (99, 98)
    """
    a,b = 99,98
    try:
        a,b = t
    except ValueError:
        pass
    return (a,b)

def test_overwrite_int(t):
    """
    >>> test_overwrite_int(l)
    (99, 98)
    >>> test_overwrite_int(t)
    (99, 98)
    """
    cdef int a,b
    a,b = 99,98
    try:
        a,b = t
    except ValueError:
        pass
    return (a,b)

def test_overwrite_mixed(t):
    """
    >>> test_overwrite_mixed(l)
    (99, 98)
    >>> test_overwrite_mixed(t)
    (99, 98)
    """
    cdef int b
    a,b = 99,98
    try:
        a,b = t
    except ValueError:
        pass
    return (a,b)

def test_overwrite_mixed2(t):
    """
    >>> test_overwrite_mixed2(l)
    (99, 98)
    >>> test_overwrite_mixed2(t)
    (99, 98)
    """
    cdef int a
    a,b = 99,98
    try:
        a,b = t
    except ValueError:
        pass
    return (a,b)
