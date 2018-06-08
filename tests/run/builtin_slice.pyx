# mode: run

def slice1(stop):
    """
    >>> list(range(8))
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> list(range(10))[slice1(8)]
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> slice1(1)
    slice(None, 1, None)
    >>> slice1(10)
    slice(None, 10, None)
    >>> slice1(None)
    slice(None, None, None)
    >>> slice1(1) == slice(1)
    True
    >>> slice1(None) == slice(None)
    True
    """
    return slice(stop)


def slice1_const():
    """
    >>> slice1_const() == slice(12)
    True
    """
    return slice(12)


def slice2(start, stop):
    """
    >>> list(range(2, 8))
    [2, 3, 4, 5, 6, 7]
    >>> list(range(10))[slice2(2, 8)]
    [2, 3, 4, 5, 6, 7]
    >>> slice2(1, 10)
    slice(1, 10, None)
    >>> slice2(None, 10)
    slice(None, 10, None)
    >>> slice2(4, None)
    slice(4, None, None)
    """
    return slice(start, stop)


def slice2_const():
    """
    >>> slice2_const() == slice(None, 12)
    True
    """
    return slice(None, 12)


def slice3(start, stop, step):
    """
    >>> list(range(2, 8, 3))
    [2, 5]
    >>> list(range(10))[slice3(2, 8, 3)]
    [2, 5]
    >>> slice3(2, None, 3)
    slice(2, None, 3)
    >>> slice3(None, 3, 2)
    slice(None, 3, 2)
    """
    return slice(start, stop, step)


def slice3_const():
    """
    >>> slice3_const() == slice(12, None, 34)
    True
    """
    return slice(12, None, 34)
