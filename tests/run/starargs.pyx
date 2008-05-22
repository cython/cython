__doc__ = u"""
    >>> spam(1,2,3)
    (1, 2, 3)
    >>> spam(1,2) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (2 given)
    >>> spam(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (4 given)
    >>> spam(1,2,3, a=1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function

    >>> grail(1,2,3)
    (1, 2, 3, ())
    >>> grail(1,2,3,4)
    (1, 2, 3, (4,))
    >>> grail(1,2,3,4,5,6,7,8,9)
    (1, 2, 3, (4, 5, 6, 7, 8, 9))
    >>> grail(1,2) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (2 given)
    >>> grail(1,2,3, a=1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function

    >>> swallow(1,2,3)
    (1, 2, 3, ())
    >>> swallow(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes at most 3 positional arguments (4 given)
    >>> swallow(1,2,3, a=1, b=2)
    (1, 2, 3, (('a', 1), ('b', 2)))
    >>> swallow(1,2,3, x=1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: keyword parameter 'x' was given by position and by name

    >>> creosote(1,2,3)
    (1, 2, 3, (), ())
    >>> creosote(1,2,3,4)
    (1, 2, 3, (4,), ())
    >>> creosote(1,2,3, a=1)
    (1, 2, 3, (), (('a', 1),))
    >>> creosote(1,2,3,4, a=1, b=2)
    (1, 2, 3, (4,), (('a', 1), ('b', 2)))
    >>> creosote(1,2,3,4, x=1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: keyword parameter 'x' was given by position and by name

    >>> onlyt(1)
    (1,)
    >>> onlyt(1,2)
    (1, 2)
    >>> onlyt(a=1)
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function
    >>> onlyt(1, a=2)
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function

    >>> onlyk(a=1)
    (('a', 1),)
    >>> onlyk(a=1, b=2)
    (('a', 1), ('b', 2))
    >>> onlyk(1)
    Traceback (most recent call last):
    TypeError: function takes at most 0 positional arguments (1 given)
    >>> onlyk(1, 2)
    Traceback (most recent call last):
    TypeError: function takes at most 0 positional arguments (2 given)
    >>> onlyk(1, a=1, b=2)
    Traceback (most recent call last):
    TypeError: function takes at most 0 positional arguments (1 given)

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

import sys, re
if sys.version_info >= (2,6):
    __doc__ = re.sub(u"Error: (.*)exactly(.*)", u"Error: \\1at most\\2", __doc__)

import sys, re
if sys.version_info >= (2,6):
    __doc__ = re.sub(u"(ELLIPSIS[^>]*Error: )[^\n]*\n", u"\\1...\n", __doc__, re.M)

cdef sorteditems(d):
    l = list(d.items())
    l.sort()
    return tuple(l)

def spam(x, y, z):
    return (x, y, z)

def grail(x, y, z, *a):
    return (x, y, z, a)

def swallow(x, y, z, **k):
    return (x, y, z, sorteditems(k))

def creosote(x, y, z, *a, **k):
    return (x, y, z, a, sorteditems(k))

def onlyt(*a):
    return a

def onlyk(**k):
    return sorteditems(k)

def tk(*a, **k):
    return a + sorteditems(k)
