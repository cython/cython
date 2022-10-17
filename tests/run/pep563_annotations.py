# mode: run
# tag: pep563, pure3.7

from __future__ import annotations

def f(a: 1+2==3, b: list, c: this_cant_evaluate, d: "Hello from inside a string") -> "Return me!":
    """
    The absolute exact strings aren't reproducible according to the PEP,
    so be careful to avoid being too specific
    >>> stypes = (type(""), type(u"")) # Python 2 is a bit awkward here
    >>> eval(f.__annotations__['a'])
    True
    >>> isinstance(f.__annotations__['a'], stypes)
    True
    >>> print(f.__annotations__['b'])
    list
    >>> print(f.__annotations__['c'])
    this_cant_evaluate
    >>> isinstance(eval(f.__annotations__['d']), stypes)
    True
    >>> print(f.__annotations__['return'][1:-1]) # First and last could be either " or '
    Return me!
    >>> f.__annotations__['return'][0] == f.__annotations__['return'][-1]
    True
    """
    pass


def empty_decorator(cls):
    return cls


@empty_decorator
class DecoratedStarship(object):
    """
    >>> sorted(DecoratedStarship.__annotations__.items())
    [('captain', 'str'), ('damage', 'cython.int')]
    """
    captain: str = 'Picard'               # instance variable with default
    damage: cython.int                    # instance variable without default
