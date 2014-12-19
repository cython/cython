# mode: run
# tag: kwargs, call
# ticket: 717

def f(**kwargs):
    return sorted(kwargs.items())

def test_call(kwargs):
    """
    >>> kwargs = {'b' : 2}
    >>> f(a=1, **kwargs)
    [('a', 1), ('b', 2)]
    >>> test_call(kwargs)
    [('a', 1), ('b', 2)]

    >>> kwargs = {'a' : 2}
    >>> f(a=1, **kwargs)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...got multiple values for keyword argument 'a'

    >>> test_call(kwargs)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...got multiple values for keyword argument 'a'
    """
    return f(a=1, **kwargs)
