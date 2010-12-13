def c(a=10, b=20, **kwds):
    """
    >>> c()
    10 20 0
    >>> c(1)
    1 20 0
    >>> c(1,2)
    1 2 0
    >>> c(key=None)
    10 20 1
    >>> c(1, key=None)
    1 20 1
    >>> c(1,2, key=None)
    1 2 1
    """
    print a, b, len(kwds)

def d(a, b=1, *args, **kwds):
    """
    >>> d()
    Traceback (most recent call last):
    TypeError: d() takes at least 1 positional argument (0 given)
    >>> d(1)
    1 1 0 0
    >>> d(1,2)
    1 2 0 0
    >>> d(1,2,3)
    1 2 1 0
    >>> d(key=None)
    Traceback (most recent call last):
    TypeError: d() takes at least 1 positional argument (0 given)
    >>> d(1, key=None)
    1 1 0 1
    >>> d(1,2, key=None)
    1 2 0 1
    >>> d(1,2,3, key=None)
    1 2 1 1
    """
    print a, b, len(args), len(kwds)

def e(*args, **kwargs):
    print len(args), len(kwargs)

def f(*args):
    """
    >>> f(1,2, d=5)
    Traceback (most recent call last):
    TypeError: f() got an unexpected keyword argument 'd'
    >>> f(1, d=5)
    Traceback (most recent call last):
    TypeError: f() got an unexpected keyword argument 'd'
    >>> f(d=5)
    Traceback (most recent call last):
    TypeError: f() got an unexpected keyword argument 'd'
    """
    print len(args)

def g(**kwargs):
    """
    >>> g(1,2, d=5)
    Traceback (most recent call last):
    TypeError: g() takes exactly 0 positional arguments (2 given)
    >>> g(1,2)
    Traceback (most recent call last):
    TypeError: g() takes exactly 0 positional arguments (2 given)
    >>> g(1)
    Traceback (most recent call last):
    TypeError: g() takes exactly 0 positional arguments (1 given)
    """
    print len(kwargs)

def h(a, b, c, *args, **kwargs):
    """
    >>> h(1,2, d=5)
    Traceback (most recent call last):
    TypeError: h() takes at least 3 positional arguments (2 given)
    """
    print a, b, c, u'*', len(args), len(kwargs)

args = (9,8,7)

import sys
if sys.version_info[0] >= 3:
    kwargs = {u"test" : u"toast"}
else:
    kwargs = {"test" : u"toast"}

def test_kw_args(f):
    """
    >>> test_kw_args(h)
    1 2 3 * 0 0
    1 2 9 * 2 1
    1 2 7 * 2 1
    1 2 9 * 2 2
    1 2 9 * 2 2
    1 2 9 * 2 3
    >>> test_kw_args(e)
    2 1
    5 1
    5 1
    5 2
    5 2
    5 3
    """
    f(1,2, c=3)
    f(1,2, d=3, *args)
    f(1,2, d=3, *(7,8,9))
    f(1,2, d=3, *args, **kwargs)
    f(1,2, d=3, *args, e=5)
    f(1,2, d=3, *args, e=5, **kwargs)

def test_pos_args(f):
    """
    >>> test_pos_args(h)
    1 2 3 * 0 0
    1 2 9 * 2 0
    1 2 7 * 2 0
    9 8 7 * 0 0
    7 8 9 * 0 0
    >>> test_pos_args(f)
    3
    5
    5
    3
    3
    """
    f(1,2,3)
    f(1,2, *args)
    f(1,2, *(7,8,9))
    f(*args)
    f(*(7,8,9))

def test_kw(f):
    """
    >>> test_kw(e)
    0 1
    0 2
    0 2
    0 1
    >>> test_kw(g)
    1
    2
    2
    1
    """
    f(c=3)
    f(d=3, e=5)
    f(d=3, **kwargs)
    f(**kwargs)

def test_noargs(f):
    """
    >>> test_noargs(e)
    0 0
    >>> test_noargs(f)
    0
    >>> test_noargs(g)
    0

    # and some errors:
    >>> test_noargs(h)
    Traceback (most recent call last):
    TypeError: h() takes at least 3 positional arguments (0 given)
    """
    f()

def test_int_kwargs(f):
    """
    >>> test_int_kwargs(e)
    Traceback (most recent call last):
    TypeError: e() keywords must be strings
    >>> test_int_kwargs(f)
    Traceback (most recent call last):
    TypeError: f() keywords must be strings
    >>> test_int_kwargs(g)
    Traceback (most recent call last):
    TypeError: g() keywords must be strings
    >>> test_int_kwargs(h)
    Traceback (most recent call last):
    TypeError: h() keywords must be strings
    """
    f(a=1,b=2,c=3, **{10:20,30:40})
