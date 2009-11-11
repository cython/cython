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

    >>> in_sequence(1, None)
    Traceback (most recent call last):
    ...
    TypeError: argument of type 'NoneType' is not iterable

    >>> in_sequence(1, 1)
    Traceback (most recent call last):
    ...
    TypeError: argument of type 'int' is not iterable
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

    >>> not_in_sequence(1, None)
    Traceback (most recent call last):
    ...
    TypeError: argument of type 'NoneType' is not iterable

    >>> not_in_sequence(1, 1)
    Traceback (most recent call last):
    ...
    TypeError: argument of type 'int' is not iterable
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
