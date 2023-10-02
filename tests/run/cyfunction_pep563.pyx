# cython: binding=True
# mode: run
# tag: cyfunction

from __future__ import annotations

# copied from cyfunction.pyx but run with the annotations future import

def test_annotations(a: "test", b: "other" = 2, c: 123 = 4) -> "ret":
    """
    >>> isinstance(test_annotations.__annotations__, dict)
    True
    >>> sorted(test_annotations.__annotations__.items())
    [('a', "'test'"), ('b', "'other'"), ('c', '123'), ('return', "'ret'")]

    >>> def func_b(): return 42
    >>> def func_c(): return 99
    >>> inner = test_annotations(1, func_b, func_c)
    >>> sorted(inner.__annotations__.items())
    [('return', 'c()'), ('x', "'banana'"), ('y', 'b()')]

    >>> inner.__annotations__ = {234: 567}
    >>> inner.__annotations__
    {234: 567}
    >>> inner.__annotations__ = None
    >>> inner.__annotations__
    {}
    >>> inner.__annotations__ = 321
    Traceback (most recent call last):
    TypeError: __annotations__ must be set to a dict object
    >>> inner.__annotations__
    {}

    >>> inner = test_annotations(1, func_b, func_c)
    >>> sorted(inner.__annotations__.items())
    [('return', 'c()'), ('x', "'banana'"), ('y', 'b()')]
    >>> inner.__annotations__['abc'] = 66
    >>> sorted(inner.__annotations__.items())
    [('abc', 66), ('return', 'c()'), ('x', "'banana'"), ('y', 'b()')]

    >>> inner = test_annotations(1, func_b, func_c)
    >>> sorted(inner.__annotations__.items())
    [('return', 'c()'), ('x', "'banana'"), ('y', 'b()')]
    """
    def inner(x: "banana", y: b()) -> c():
        return x,y
    return inner
