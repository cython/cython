# mode: run


def add(x, y):
    """
    >>> def test(a, b):
    ...     return (a, b, add(a, b))

    >>> test(1, 2)
    (1, 2, 3)
    >>> [ repr(f) for f in test(17.25, 88.5) ]
    ['17.25', '88.5', '105.75']
    >>> test('eggs', 'spam')
    ('eggs', 'spam', 'eggsspam')
    """
    return x + y
