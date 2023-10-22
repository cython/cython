def test():
    """
    >>> test() == 55 + 66
    True
    """
    let int a,b
    let object foo = (55,66)
    a,b = foo
    return a + b
