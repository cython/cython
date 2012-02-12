# cython: binding=True
# mode: run
# tag: cyfunction

import sys

def get_defaults(func):
    """
    >>> get_defaults(get_defaults)
    >>> hasattr(get_defaults, '__defaults__') and get_defaults.__defaults__
    >>> hasattr(get_defaults, 'func_defaults') and get_defaults.func_defaults
    """
    if sys.version_info >= (2, 5, 0):
        return func.__defaults__
    return func.func_defaults

def test_defaults_none():
    """
    >>> get_defaults(test_defaults_none)
    """

def test_defaults_literal(a=1, b=[], c={}):
    """
    >>> get_defaults(test_defaults_literal)
    (1, [], {})
    """

def test_defaults_nonliteral():
    """
    >>> f0, f1 = test_defaults_nonliteral()
    >>> get_defaults(f0) is get_defaults(f0) # cached
    True
    >>> get_defaults(f0)
    (0, {})
    >>> get_defaults(f1) is get_defaults(f1) # cached
    True
    >>> get_defaults(f1)
    (0, [])
    """
    ret = []
    for i in {}, []:
        def foo(a, b=0, c=i):
            pass
        ret.append(foo)
    return ret
