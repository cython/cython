# ticket: t544

def count(i=[0]):
    i[0] += 1
    return i[0]

def test(x):
    """
    >>> def py_count(i=[0]):
    ...     i[0] += 1
    ...     return i[0]
    >>> 1 in (py_count(), py_count(), py_count(), py_count())
    True
    >>> 4 in (py_count(), py_count(), py_count(), py_count())
    False
    >>> 12 in (py_count(), py_count(), py_count(), py_count())
    True

    >>> test(1)
    True
    >>> test(4)
    False
    >>> test(12)
    True
    """
    return x in (count(), count(), count(), count())
