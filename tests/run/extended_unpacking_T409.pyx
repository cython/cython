# ticket: 409

def simple():
    """
    >>> simple()
    ([1, 2], [1, 2])
    """
    d = e = [1,2]
    return d, e

def simple_parallel():
    """
    >>> simple_parallel()
    (1, 2, [1, 2], [1, 2])
    """
    a, c = d = e = [1,2]
    return a, c, d, e

def extended():
    """
    >>> extended()
    (1, [], 2, [1, 2], [1, 2])
    """
    a, *b, c = d = e = [1,2]
    return a, b, c, d, e
