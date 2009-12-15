def b(a, b, c):
    """
    >>> b(1,2,3)
    >>> b(1,2,3,4)
    Traceback (most recent call last):
    TypeError: b() takes exactly 3 positional arguments (4 given)
    """
    a, b, c = b, c, a

def c(a, b, c=1):
    """
    >>> c(1,2)
    >>> c(1,2,3)
    >>> c(1,2,3,4)
    Traceback (most recent call last):
    TypeError: c() takes at most 3 positional arguments (4 given)
    """
    a, b, c = b, c, a

def d(a, b, *, c = 88):
    """
    >>> d(1,2)
    >>> d(1,2, c=1)
    >>> d(1,2,3)
    Traceback (most recent call last):
    TypeError: d() takes exactly 2 positional arguments (3 given)
    >>> d(1,2, d=1)
    Traceback (most recent call last):
    TypeError: d() got an unexpected keyword argument 'd'
    """
    a, b, c = b, c, a

def e(a, b, c = 88, **kwds):
    """
    >>> e(1,2)
    >>> e(1,2, c=1)
    >>> e(1,2, d=1)
    >>> e(1,2, c=1, d=2, e=3)
    >>> e(1,2,3)
    >>> e(1,2,3,4)
    Traceback (most recent call last):
    TypeError: e() takes at most 3 positional arguments (4 given)
    """
    a, b, c = b, c, a

def f(a, b, *, c, d = 42):
    """
    >>> f(1,2, c=1)
    >>> f(1,2, c=1, d=2)
    >>> f(1,2,3)
    Traceback (most recent call last):
    TypeError: f() takes exactly 2 positional arguments (3 given)
    >>> f(1,2)
    Traceback (most recent call last):
    TypeError: f() needs keyword-only argument c
    >>> f(1,2, c=1, e=2)
    Traceback (most recent call last):
    TypeError: f() got an unexpected keyword argument 'e'
    """
    a, b, c, d = b, c, d, a

def g(a, b, *, c, d = 42, e = 17, f, **kwds):
    """
    >>> g(1,2, c=1, f=2)
    >>> g(1,2, c=1, e=0, f=2, d=11)
    >>> g(1,2, c=1, f=2, e=0, x=25)
    >>> g(1,2,3)
    Traceback (most recent call last):
    TypeError: g() takes exactly 2 positional arguments (3 given)
    >>> g(1,2)
    Traceback (most recent call last):
    TypeError: g() needs keyword-only argument c
    >>> g(1,2, c=1)
    Traceback (most recent call last):
    TypeError: g() needs keyword-only argument f
    """
    a, b, c, d, e, f = b, c, d, e, f, a

def h(a, b, *args, c, d = 42, e = 17, f, **kwds):
    """
    >>> h(1,2, c=1, f=2)
    >>> h(1,2, c=1, f=2, e=3)
    >>> h(1,2,3,4,5,6, c=1, f=2)
    >>> h(1,2,3,4,5,6, c=1, f=2, e=3, x=25, y=11)
    >>> h(1,2,3)
    Traceback (most recent call last):
    TypeError: h() needs keyword-only argument c
    >>> h(1,2, d=1)
    Traceback (most recent call last):
    TypeError: h() needs keyword-only argument c
    """
    a, b, c, d, e, f = b, c, d, e, f, a

def k(a, b, c=1, *args, d = 42, e = 17, f, **kwds):
    """
    >>> k(1,2, c=1, f=2)
    >>> k(1,2, c=1, f=2, e=3)
    >>> k(1,2,3,4,5,6, d=1, f=2)
    >>> k(1,2,3,4,5,6, d=1, f=2, e=3, x=25, y=11)
    >>> k(1,2,3)
    Traceback (most recent call last):
    TypeError: k() needs keyword-only argument f
    >>> k(1,2, d=1)
    Traceback (most recent call last):
    TypeError: k() needs keyword-only argument f
    """
    a, b, c, d, e, f = b, c, d, e, f, a

def l(*, a, b, c = 88):
    """
    >>> l(a=1, b=2)
    >>> l(a=1, b=2, c=1)
    >>> l(1,2,3)
    Traceback (most recent call last):
    TypeError: l() takes exactly 0 positional arguments (3 given)
    >>> l(1,2, d=1)
    Traceback (most recent call last):
    TypeError: l() takes exactly 0 positional arguments (2 given)
    >>> l(1,2,3)
    Traceback (most recent call last):
    TypeError: l() takes exactly 0 positional arguments (3 given)
    >>> l(1,2, d=1)
    Traceback (most recent call last):
    TypeError: l() takes exactly 0 positional arguments (2 given)
    """
    a, b, c = b, c, a

def m(a, *, b, c = 88):
    """
    >>> m(1, b=2)
    >>> m(a=1, b=2)
    >>> m(a=1, b=2, c=1)
    """
    a, b, c = b, c, a

def n(a, *, b, c = 88):
    a, b, c = b, c, a
