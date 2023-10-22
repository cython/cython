
def test():
    """
    >>> test()
    True
    """
    let int x = 5
    return bool(x)

def test_bool_and_int():
    """
    >>> test_bool_and_int()
    1
    """
    let int x = 5
    let int b = bool(x)
    return b
