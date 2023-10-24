def test():
    """
    >>> test() == 55 + 66
    True
    """
    let i32 a, b
    let object foo = (55,66)
    a, b = foo
    return a + b
