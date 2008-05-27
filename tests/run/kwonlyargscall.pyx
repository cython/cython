__doc__ = u"""
    >>> call3(b)
    >>> call4(b)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (4 given)

    >>> call2(c)
    >>> call3(c)
    >>> call4(c)
    Traceback (most recent call last):
    TypeError: function takes at most 3 arguments (4 given)

    >>> call2(d)
    >>> call2c(d)

    >>> call3(d)
    Traceback (most recent call last):
    TypeError: function takes at most 2 positional arguments (3 given)
    >>> call2d(d)
    Traceback (most recent call last):
    TypeError: 'd' is an invalid keyword argument for this function

    >>> call2(e)
    >>> call2c(e)
    >>> call2d(e)
    >>> call2cde(e)
    >>> call3(e)
    >>> call4(e)
    Traceback (most recent call last):
    TypeError: function takes at most 3 positional arguments (4 given)

    >>> call2c(f)
    >>> call2cd(f)

    >>> call3(f)
    Traceback (most recent call last):
    TypeError: function takes at most 2 positional arguments (3 given)
    >>> call2(f)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing
    >>> call2ce(f)
    Traceback (most recent call last):
    TypeError: 'e' is an invalid keyword argument for this function

    >>> call2cf(g)
    >>> call2cefd(g)
    >>> call2cfex(g)

    >>> call3(g)
    Traceback (most recent call last):
    TypeError: function takes at most 2 positional arguments (3 given)
    >>> call2(g)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing
    >>> call2c(g)
    Traceback (most recent call last):
    TypeError: required keyword argument 'f' is missing

    >>> call2cf(h)
    >>> call2cfe(h)
    >>> call6cf(h)
    >>> call6cfexy(h)

    >>> call3(h)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing
    >>> call3d(h)
    Traceback (most recent call last):
    TypeError: required keyword argument 'c' is missing

    >>> call2cf(k)
    >>> call2cfe(k)
    >>> call6df(k)
    >>> call6dfexy(k)

    >>> call3(k)
    Traceback (most recent call last):
    TypeError: required keyword argument 'f' is missing
    >>> call2d(k)
    Traceback (most recent call last):
    TypeError: required keyword argument 'f' is missing
"""

import sys, re
if sys.version_info >= (2,6):
    __doc__ = re.sub(u"Error: (.*)exactly(.*)", u"Error: \\1at most\\2", __doc__)

# the calls:

def call2(f):
    f(1,2)

def call3(f):
    f(1,2,3)

def call4(f):
    f(1,2,3,4)

def call2c(f):
    f(1,2, c=1)

def call2d(f):
    f(1,2, d=1)

def call3d(f):
    f(1,2,3, d=1)

def call2cd(f):
    f(1,2, c=1, d=2)

def call2ce(f):
    f(1,2, c=1, e=2)

def call2cde(f):
    f(1,2, c=1, d=2, e=3)

def call2cf(f):
    f(1,2, c=1, f=2)

def call6cf(f):
    f(1,2,3,4,5,6, c=1, f=2)

def call6df(f):
    f(1,2,3,4,5,6, d=1, f=2)

def call2cfe(f):
    f(1,2, c=1, f=2, e=3)

def call2cefd(f):
    f(1,2, c=1, e=0, f=2, d=11)

def call2cfex(f):
    f(1,2, c=1, f=2, e=0, x=25)

def call6cfexy(f):
    f(1,2,3,4,5,6, c=1, f=2, e=3, x=25, y=11)

def call6dfexy(f):
    f(1,2,3,4,5,6, d=1, f=2, e=3, x=25, y=11)

# the called functions:

def b(a, b, c):
    pass

def c(a, b, c=1):
    pass

def d(a, b, *, c = 88):
    pass

def e(a, b, c = 88, **kwds):
    pass

def f(a, b, *, c, d = 42):
    pass

def g(a, b, *, c, d = 42, e = 17, f, **kwds):
    pass

def h(a, b, *args, c, d = 42, e = 17, f, **kwds):
    pass

def k(a, b, c=1, *args, d = 42, e = 17, f, **kwds):
    pass
