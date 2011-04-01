# ticket: 664

def assign():
    """
    >>> assign()
    (1, [2, 3, 4, 5])
    """
    a, *b = 1, 2, 3, 4, 5
    return a, b

def assign3():
    """
    >>> assign3()
    (1, [2, 3, 4, 5], 6)
    """
    a, *b, c = 1, 2, 3, 4, 5, 6
    return a, b, c

def assign4():
    """
    >>> assign4()
    (1, [2, 3, 4], 5, 6)
    """
    a, *b, c, d = 1, 2, 3, 4, 5, 6
    return a, b, c, d
