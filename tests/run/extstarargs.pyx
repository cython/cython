__doc__ = u"""
    >>> s = Silly(1,2,3, 'test')
    >>> (spam,grail,swallow,creosote,onlyt,onlyk,tk) = (
    ...     s.spam,s.grail,s.swallow,s.creosote,s.onlyt,s.onlyk,s.tk)

    >>> spam(1,2,3)
    (1, 2, 3)
    >>> spam(1,2)
    Traceback (most recent call last):
    TypeError: spam() takes exactly 3 positional arguments (2 given)
    >>> spam(1,2,3,4)
    Traceback (most recent call last):
    TypeError: spam() takes exactly 3 positional arguments (4 given)
    >>> spam(1,2,3, a=1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: spam() got an unexpected keyword argument 'a'

    >>> grail(1,2,3)
    (1, 2, 3, ())
    >>> grail(1,2,3,4)
    (1, 2, 3, (4,))
    >>> grail(1,2,3,4,5,6,7,8,9)
    (1, 2, 3, (4, 5, 6, 7, 8, 9))
    >>> grail(1,2)
    Traceback (most recent call last):
    TypeError: grail() takes at least 3 positional arguments (2 given)
    >>> grail(1,2,3, a=1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: grail() got an unexpected keyword argument 'a'

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
    __doc__ = re.sub(u"(ELLIPSIS[^>]*Error: )[^\n]*\n", u"\\1...\n", __doc__)

cdef sorteditems(d):
    l = list(d.items())
    l.sort()
    return tuple(l)

cdef class Silly:

    def __init__(self, *a):
        pass

    def spam(self, x, y, z):
        return (x, y, z)

    def grail(self, x, y, z, *a):
        return (x, y, z, a)

    def swallow(self, x, y, z, **k):
        return (x, y, z, sorteditems(k))

    def creosote(self, x, y, z, *a, **k):
        return (x, y, z, a, sorteditems(k))

    def onlyt(self, *a):
        return a

    def onlyk(self, **k):
        return sorteditems(k)

    def tk(self, *a, **k):
        return a + sorteditems(k)
