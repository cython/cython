# mode: run
# ticket: 674

def test_inner(a):
    """
    >>> a = test_inner(1)
    >>> b = test_inner(2)
    >>> a()
    1
    >>> b()
    2
    """
    def inner(b=a):
        return b
    return inner

def test_lambda(n):
    """
    >>> [f() for f in test_lambda(3)]
    [0, 1, 2]
    """
    return [lambda v=i: v for i in range(n)]
