def test_str_subclass_kwargs(k=None):
    """
    Test passing keywords with names that are not of type ``str``
    but a subclass:

    >>> class StrSubclass(str):
    ...     pass
    >>> class StrNoCompare(str):
    ...     def __eq__(self, other):
    ...         raise RuntimeError("do not compare me")
    ...     def __hash__(self):
    ...         return hash(str(self))
    >>> kwargs = {StrSubclass('k'): 'value'}
    >>> test_str_subclass_kwargs(**kwargs)
    'value'
    >>> kwargs = {StrNoCompare('k'): 'value'}
    >>> test_str_subclass_kwargs(**kwargs)
    Traceback (most recent call last):
    RuntimeError: do not compare me
    """
    return k
