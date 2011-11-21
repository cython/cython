def test(dict d, index):
    """
    >>> d = { 1: 10 }
    >>> test(d, 1)
    10

    >>> test(d, 2)
    Traceback (most recent call last):
    KeyError: 2

    >>> test(d, (1,2))
    Traceback (most recent call last):
    KeyError: (1, 2)

    >>> class Unhashable:
    ...    def __hash__(self):
    ...        raise ValueError
    >>> test(d, Unhashable())
    Traceback (most recent call last):
    ValueError

    >>> test(None, 1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...object...
    """
    return d[index]

cdef class Subscriptable:
    def __getitem__(self, key):
        return key


def getitem_in_condition(dict d, key, expected_result):
    """
    >>> d = dict(a=1, b=2)
    >>> getitem_in_condition(d, 'a', 1)
    True
    """
    return d[key] is expected_result
