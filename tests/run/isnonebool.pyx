def test_and(a,b):
    """
    >>> test_and(None, None)
    True
    >>> test_and(None, 1)
    False
    >>> test_and(1, None)
    False
    """
    return a is None and b is None

def test_more(a,b):
    """
    >>> test_more(None, None)
    True
    >>> test_more(None, 1)
    True
    >>> test_more(1, None)
    False
    >>> test_more(None, 0)
    False
    """
    return a is None and (b is None or b == 1)

def test_more_c(a,b):
    """
    >>> test_more_c(None, None)
    True
    >>> test_more_c(None, 1)
    True
    >>> test_more_c(1, None)
    False
    >>> test_more_c(None, 0)
    False
    """
    return (a is None or 1 == 2) and (b is None or b == 1)
