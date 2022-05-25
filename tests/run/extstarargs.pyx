cimport cython

cdef sorteditems(d):
    return tuple(sorted(d.items()))


cdef class Silly:

    def __init__(self, *a):
        """
        >>> s = Silly(1,2,3, 'test')
        """

    def spam(self, x, y, z):
        """
        >>> s = Silly()
        >>> s.spam(1,2,3)
        (1, 2, 3)
        >>> s.spam(1,2)
        Traceback (most recent call last):
        TypeError: spam() takes exactly 3 positional arguments (2 given)
        >>> s.spam(1,2,3,4)
        Traceback (most recent call last):
        TypeError: spam() takes exactly 3 positional arguments (4 given)
        >>> s.spam(1,2,3, a=1)
        Traceback (most recent call last):
        TypeError: spam() got an unexpected keyword argument 'a'
        """
        return (x, y, z)

    def grail(self, x, y, z, *a):
        """
        >>> s = Silly()
        >>> s.grail(1,2,3)
        (1, 2, 3, ())
        >>> s.grail(1,2,3,4)
        (1, 2, 3, (4,))
        >>> s.grail(1,2,3,4,5,6,7,8,9)
        (1, 2, 3, (4, 5, 6, 7, 8, 9))
        >>> s.grail(1,2)
        Traceback (most recent call last):
        TypeError: grail() takes at least 3 positional arguments (2 given)
        >>> s.grail(1,2,3, a=1)
        Traceback (most recent call last):
        TypeError: grail() got an unexpected keyword argument 'a'
        """
        return (x, y, z, a)

    def swallow(self, x, y, z, **k):
        """
        >>> s = Silly()
        >>> s.swallow(1,2,3)
        (1, 2, 3, ())
        >>> s.swallow(1,2,3,4)
        Traceback (most recent call last):
        TypeError: swallow() takes exactly 3 positional arguments (4 given)
        >>> s.swallow(1,2,3, a=1, b=2)
        (1, 2, 3, (('a', 1), ('b', 2)))
        >>> s.swallow(1,2,3, x=1)
        Traceback (most recent call last):
        TypeError: swallow() got multiple values for keyword argument 'x'
        """
        return (x, y, z, sorteditems(k))

    def creosote(self, x, y, z, *a, **k):
        """
        >>> s = Silly()
        >>> s.creosote(1,2,3)
        (1, 2, 3, (), ())
        >>> s.creosote(1,2,3,4)
        (1, 2, 3, (4,), ())
        >>> s.creosote(1,2,3, a=1)
        (1, 2, 3, (), (('a', 1),))
        >>> s.creosote(1,2,3,4, a=1, b=2)
        (1, 2, 3, (4,), (('a', 1), ('b', 2)))
        >>> s.creosote(1,2,3,4, x=1)
        Traceback (most recent call last):
        TypeError: creosote() got multiple values for keyword argument 'x'
        """
        return (x, y, z, a, sorteditems(k))

    def onlyt(self, *a):
        """
        >>> s = Silly()
        >>> s.onlyt(1)
        (1,)
        >>> s.onlyt(1,2)
        (1, 2)
        >>> s.onlyt(a=1)
        Traceback (most recent call last):
        TypeError: onlyt() got an unexpected keyword argument 'a'
        >>> s.onlyt(1, a=2)
        Traceback (most recent call last):
        TypeError: onlyt() got an unexpected keyword argument 'a'
        """
        return a

    @cython.binding(False)  # passthrough of exact same tuple can't work with binding
    def onlyt_nobinding(self, *a):
        """
        >>> s = Silly()
        >>> s.onlyt_nobinding(1)
        (1,)
        >>> s.onlyt_nobinding(1,2)
        (1, 2)
        >>> s.onlyt_nobinding(a=1)
        Traceback (most recent call last):
        TypeError: onlyt_nobinding() got an unexpected keyword argument 'a'
        >>> s.onlyt_nobinding(1, a=2)
        Traceback (most recent call last):
        TypeError: onlyt_nobinding() got an unexpected keyword argument 'a'
        >>> test_no_copy_args(s.onlyt_nobinding)
        True
        """
        return a

    def onlyk(self, **k):
        """
        >>> s = Silly()
        >>> s.onlyk(a=1)
        (('a', 1),)
        >>> s.onlyk(a=1, b=2)
        (('a', 1), ('b', 2))
        >>> s.onlyk(1)
        Traceback (most recent call last):
        TypeError: onlyk() takes exactly 0 positional arguments (1 given)
        >>> s.onlyk(1, 2)
        Traceback (most recent call last):
        TypeError: onlyk() takes exactly 0 positional arguments (2 given)
        >>> s.onlyk(1, a=1, b=2)
        Traceback (most recent call last):
        TypeError: onlyk() takes exactly 0 positional arguments (1 given)
        """
        return sorteditems(k)

    def tk(self, *a, **k):
        """
        >>> s = Silly()
        >>> s.tk(a=1)
        (('a', 1),)
        >>> s.tk(a=1, b=2)
        (('a', 1), ('b', 2))
        >>> s.tk(1)
        (1,)
        >>> s.tk(1, 2)
        (1, 2)
        >>> s.tk(1, a=1, b=2)
        (1, ('a', 1), ('b', 2))
        """
        return a + sorteditems(k)

    @cython.binding(False)  # passthrough of exact same tuple can't work with binding
    def t_kwonly(self, *a, k):
        """
        >>> s = Silly()
        >>> test_no_copy_args(s.t_kwonly, k=None)
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
