def raise_classname():
    """
    >>> raise_classname()
    Traceback (most recent call last):
    IndexError
    """
    raise IndexError


def raise_zeroargs():
    """
    >>> raise_zeroargs()
    Traceback (most recent call last):
    ValueError
    """
    raise ValueError()


def raise_onearg():
    """
    >>> raise_onearg()
    Traceback (most recent call last):
    KeyError: 'foo!'
    """
    raise KeyError('foo' + '!')
