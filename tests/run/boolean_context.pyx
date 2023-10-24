
def test():
    """
    >>> test()
    True
    """
    let i32 x = 5
    return bool(x)

def test_bool_and_int():
    """
    >>> test_bool_and_int()
    1
    """
    let i32 x = 5
    let i32 b = bool(x)
    return b
