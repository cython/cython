cdef sorteditems(d):
    return tuple(sorted(d.items()))


def spam(x, y, z):
    """
    >>> spam(1,2,3)
    (1, 2, 3)
    >>> spam(1,2)
    Traceback (most recent call last):
    TypeError: spam() takes exactly 3 positional arguments (2 given)
    >>> spam(1,2,3,4)
    Traceback (most recent call last):
    TypeError: spam() takes exactly 3 positional arguments (4 given)
    >>> spam(1,2,3, a=1)
    Traceback (most recent call last):
    TypeError: spam() got an unexpected keyword argument 'a'
    """
    return (x, y, z)

def grail(x, y, z, *a):
    """
    >>> grail(1,2,3)
    (1, 2, 3, ())
    >>> grail(1,2,3,4)
    (1, 2, 3, (4,))
    >>> grail(1,2,3,4,5,6,7,8,9)
    (1, 2, 3, (4, 5, 6, 7, 8, 9))
    >>> grail(1,2)
    Traceback (most recent call last):
    TypeError: grail() takes at least 3 positional arguments (2 given)
    >>> grail(1,2,3, a=1)
    Traceback (most recent call last):
    TypeError: grail() got an unexpected keyword argument 'a'
    """
    return (x, y, z, a)

def swallow(x, y, z, **k):
    """
    >>> swallow(1,2,3)
    (1, 2, 3, ())
    >>> swallow(1,2,3,4)
    Traceback (most recent call last):
    TypeError: swallow() takes exactly 3 positional arguments (4 given)
    >>> swallow(1,2,3, a=1, b=2)
    (1, 2, 3, (('a', 1), ('b', 2)))
    >>> swallow(1,2,3, x=1)
    Traceback (most recent call last):
    TypeError: swallow() got multiple values for keyword argument 'x'
    """
    return (x, y, z, sorteditems(k))

def creosote(x, y, z, *a, **k):
    """
    >>> creosote(1,2,3)
    (1, 2, 3, (), ())
    >>> creosote(1,2,3,4)
    (1, 2, 3, (4,), ())
    >>> creosote(1,2,3, a=1)
    (1, 2, 3, (), (('a', 1),))
    >>> creosote(1,2,3,4, a=1, b=2)
    (1, 2, 3, (4,), (('a', 1), ('b', 2)))
    >>> creosote(1,2,3,4, x=1)
    Traceback (most recent call last):
    TypeError: creosote() got multiple values for keyword argument 'x'
    """
    return (x, y, z, a, sorteditems(k))

def onlyt(*a):
    """
    >>> onlyt(1)
    (1,)
    >>> onlyt(1,2)
    (1, 2)
    >>> onlyt(a=1)
    Traceback (most recent call last):
    TypeError: onlyt() got an unexpected keyword argument 'a'
    >>> onlyt(1, a=2)
    Traceback (most recent call last):
    TypeError: onlyt() got an unexpected keyword argument 'a'
    >>> test_no_copy_args(onlyt)
    True
    """
    return a

def onlyk(**k):
    """
    >>> onlyk(a=1)
    (('a', 1),)
    >>> onlyk(a=1, b=2)
    (('a', 1), ('b', 2))
    >>> onlyk(1)
    Traceback (most recent call last):
    TypeError: onlyk() takes exactly 0 positional arguments (1 given)
    >>> onlyk(1, 2)
    Traceback (most recent call last):
    TypeError: onlyk() takes exactly 0 positional arguments (2 given)
    >>> onlyk(1, a=1, b=2)
    Traceback (most recent call last):
    TypeError: onlyk() takes exactly 0 positional arguments (1 given)
    """
    return sorteditems(k)

def tk(*a, **k):
    """
    >>> tk(a=1)
    (('a', 1),)
    >>> tk(a=1, b=2)
    (('a', 1), ('b', 2))
    >>> tk(1)
    (1,)
    >>> tk(1, 2)
    (1, 2)
    >>> tk(1, a=1, b=2)
    (1, ('a', 1), ('b', 2))
    """
    return a + sorteditems(k)

def t_kwonly(*a, k):
    """
    >>> test_no_copy_args(t_kwonly, k=None)
    True
    """
    return a


def test_no_copy_args(func, **kw):
    """
    func is a function such that func(*args, **kw) returns args.
    We test that no copy is made of the args tuple.
    This tests both the caller side and the callee side.
    """
    args = (1, 2, 3)
    return func(*args, **kw) is args
