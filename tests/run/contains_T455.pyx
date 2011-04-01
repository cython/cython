# ticket: 455

def in_sequence(x, seq):
    """
    >>> in_sequence(1, [])
    False
    >>> in_sequence(1, ())
    False
    >>> in_sequence(1, {})
    False
    >>> in_sequence(1, [1])
    True
    >>> in_sequence(1, (1,))
    True
    >>> in_sequence(1, {1:None})
    True

    >>> in_sequence(1, None)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...

    >>> in_sequence(1, 1)       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    """
    return x in seq

def not_in_sequence(x, seq):
    """
    >>> not_in_sequence(1, [])
    True
    >>> not_in_sequence(1, ())
    True
    >>> not_in_sequence(1, {})
    True
    >>> not_in_sequence(1, [1])
    False
    >>> not_in_sequence(1, (1,))
    False
    >>> not_in_sequence(1, {1:None})
    False

    >>> not_in_sequence(1, None)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...

    >>> not_in_sequence(1, 1)       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    """
    return x not in seq


def in_dict(k, dict dct):
    """
    >>> in_dict(1, {})
    False
    >>> in_dict(1, {1:None})
    True

    >>> in_dict(1, None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not iterable
    """
    return k in dct

def not_in_dict(k, dict dct):
    """
    >>> not_in_dict(1, {})
    True
    >>> not_in_dict(1, {1:None})
    False

    >>> not_in_dict(1, None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not iterable
    """
    return k not in dct

def cascaded(a, b, c):
    """
    >>> cascaded(1, 2, 3)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...iterable...
    >>> cascaded(-1, (1,2), (1,3))
    True
    >>> cascaded(1, (1,2), (1,3))
    False
    >>> cascaded(-1, (1,2), (1,0))
    False
    """
    return a not in b < c
