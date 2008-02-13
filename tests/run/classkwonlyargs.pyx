__doc__ = """
    >>> spam = Spam()
    >>> b,c,d,e,f,g,h,k = spam.b,spam.c,spam.d,spam.e,spam.f,spam.g,spam.h,spam.k

    >>> b(1,2,3)
    >>> b(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes exactly 4 arguments (5 given)

    >>> c(1,2)
    >>> c(1,2,3)
    >>> c(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes at most 4 arguments (5 given)

    >>> d(1,2)
    >>> d(1,2, c=1)

    >>> d(1,2,3)
    Traceback (most recent call last):
    TypeError: function takes at most 3 positional arguments (4 given)
    >>> d(1,2, d=1)
    Traceback (most recent call last):
    TypeError: 'd' is an invalid keyword argument for this function

    >>> e(1,2)
    >>> e(1,2, c=1)
    >>> e(1,2, d=1)
    >>> e(1,2, c=1, d=2, e=3)
    >>> e(1,2,3)
    >>> e(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes at most 4 positional arguments (5 given)

    >>> f(1,2, c=1)
    >>> f(1,2, c=1, d=2)

    >>> f(1,2,3)
    Traceback (most recent call last):
    TypeError: function takes at most 3 positional arguments (4 given)
    >>> f(1,2)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing
    >>> f(1,2, c=1, e=2)
    Traceback (most recent call last):
    TypeError: 'e' is an invalid keyword argument for this function

    >>> g(1,2, c=1, f=2)
    >>> g(1,2, c=1, e=0, f=2, d=11)
    >>> g(1,2, c=1, f=2, e=0, x=25)

    >>> g(1,2,3)
    Traceback (most recent call last):
    TypeError: function takes at most 3 positional arguments (4 given)
    >>> g(1,2)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing
    >>> g(1,2, c=1)
    Traceback (most recent call last):
    TypeError: required keyword argument 'f' is missing

    >>> h(1,2, c=1, f=2)
    >>> h(1,2, c=1, f=2, e=3)
    >>> h(1,2,3,4,5,6, c=1, f=2)
    >>> h(1,2,3,4,5,6, c=1, f=2, e=3, x=25, y=11)

    >>> h(1,2,3)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing
    >>> h(1,2, d=1)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing

    >>> k(1,2, c=1, f=2)
    >>> k(1,2, c=1, f=2, e=3)
    >>> k(1,2,3,4,5,6, d=1, f=2)
    >>> k(1,2,3,4,5,6, d=1, f=2, e=3, x=25, y=11)

    >>> k(1,2,3)
    Traceback (most recent call last):
    TypeError: required keyword argument 'f' is missing
    >>> k(1,2, d=1)
    Traceback (most recent call last):
    TypeError: required keyword argument 'f' is missing
"""

class Spam:
    def b(self, a, b, c):
        pass

    def c(self, a, b, c=1):
        pass

    def d(self, a, b, *, c = 88):
        pass

    def e(self, a, b, c = 88, **kwds):
        pass

    def f(self, a, b, *, c, d = 42):
        pass

    def g(self, a, b, *, c, d = 42, e = 17, f, **kwds):
        pass

    def h(self, a, b, *args, c, d = 42, e = 17, f, **kwds):
        pass

    def k(self, a, b, c=1, *args, d = 42, e = 17, f, **kwds):
        pass
