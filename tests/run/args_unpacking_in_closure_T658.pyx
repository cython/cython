# mode: run
# tag: closures
# ticket: 658

def outer(int x, *args, **kwargs):
    """
    >>> inner = outer(1, 2, a=3)
    >>> inner()
    (1, (2,), {'a': 3})

    >>> inner = outer('abc', 2, a=3)
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    def inner():
        return x, args, kwargs
    return inner
