# cython: binding=True
# mode: run
# tag: cyfunction

import sys

def get_defaults(func):
    if sys.version_info >= (2, 5, 0):
        return func.__defaults__
    return func.func_defaults

def test_defaults_none():
    """
    >>> get_defaults(test_defaults_none)
    """

def test_defaults_literal(a=1, b=(1,2,3)):
    """
    >>> get_defaults(test_defaults_literal) is get_defaults(test_defaults_literal)
    True
    >>> get_defaults(test_defaults_literal)
    (1, (1, 2, 3))
    >>> a, b = get_defaults(test_defaults_literal)
    >>> c, d = test_defaults_literal()
    >>> a is c
    True
    >>> b is d
    True
    """
    return a, b

def test_defaults_nonliteral():
    """
    >>> f0, f1 = test_defaults_nonliteral()
    >>> get_defaults(f0) is get_defaults(f0) # cached
    True
    >>> get_defaults(f0)
    (0, {}, (1, 2, 3))
    >>> a, b = get_defaults(f0)[1:]
    >>> c, d = f0(0)
    >>> a is c
    True
    >>> b is d
    True
    >>> get_defaults(f1) is get_defaults(f1) # cached
    True
    >>> get_defaults(f1)
    (0, [], (1, 2, 3))
    >>> a, b = get_defaults(f1)[1:]
    >>> c, d = f1(0)
    >>> a is c
    True
    >>> b is d
    True
    """
    ret = []
    for i in {}, []:
        def foo(a, b=0, c=i, d=(1,2,3)):
            return c, d
        ret.append(foo)
    return ret
