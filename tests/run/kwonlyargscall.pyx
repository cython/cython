# the calls:

def call0ab(f):
    """
    >>> call0ab(b)
    Traceback (most recent call last):
    TypeError: b() takes exactly 3 positional arguments (2 given)
    >>> call0ab(c)
    1 2 1
    >>> call0ab(d)
    1 2 88
    """
    f(a=1,b=2)

def call0abc(f):
    """
    >>> call0abc(b)
    1 2 3
    >>> call0abc(c)
    1 2 3
    >>> call0abc(d)
    1 2 3
    >>> call0abc(e)
    1 2 3 []
    >>> call0abc(f)
    1 2 3 42
    >>> call0abc(m)
    1 2 3
    """
    f(a=1,b=2,c=3)

def call2(f):
    """
    >>> call2(c)
    1 2 1
    >>> call2(d)
    1 2 88
    >>> call2(e)
    1 2 88 []
    >>> call2(f)
    Traceback (most recent call last):
    TypeError: f() needs keyword-only argument c
    >>> call2(g)
    Traceback (most recent call last):
    TypeError: g() needs keyword-only argument c
    >>> call2(m)
    Traceback (most recent call last):
    TypeError: m() needs keyword-only argument c
    """
    f(1,2)

def call3(f):
    """
    >>> call3(b)
    1 2 3
    >>> call3(c)
    1 2 3
    >>> call3(d)
    Traceback (most recent call last):
    TypeError: d() takes exactly 2 positional arguments (3 given)
    >>> call3(e)
    1 2 3 []
    >>> call3(f)
    Traceback (most recent call last):
    TypeError: f() takes exactly 2 positional arguments (3 given)
    >>> call3(g)
    Traceback (most recent call last):
    TypeError: g() takes exactly 2 positional arguments (3 given)
    >>> call3(h)
    Traceback (most recent call last):
    TypeError: h() needs keyword-only argument c
    >>> call3(k)
    Traceback (most recent call last):
    TypeError: k() needs keyword-only argument f
    >>> call3(m)
    Traceback (most recent call last):
    TypeError: m() takes at most 2 positional arguments (3 given)
    """
    f(1,2,3)

def call4(f):
    """
    >>> call4(b)
    Traceback (most recent call last):
    TypeError: b() takes exactly 3 positional arguments (4 given)
    >>> call4(c)
    Traceback (most recent call last):
    TypeError: c() takes at most 3 positional arguments (4 given)
    >>> call4(e)
    Traceback (most recent call last):
    TypeError: e() takes at most 3 positional arguments (4 given)
    """
    f(1,2,3,4)

def call2c(f):
    """
    >>> call2c(d)
    1 2 1
    >>> call2c(e)
    1 2 1 []
    >>> call2c(f)
    1 2 1 42
    >>> call2c(g)
    Traceback (most recent call last):
    TypeError: g() needs keyword-only argument f
    >>> call2c(m)
    1 2 1
    """
    f(1,2, c=1)

def call2d(f):
    """
    >>> call2d(d)
    Traceback (most recent call last):
    TypeError: d() got an unexpected keyword argument 'd'
    >>> call2d(e)
    1 2 88 [('d', 1)]
    >>> call2d(k)
    Traceback (most recent call last):
    TypeError: k() needs keyword-only argument f
    """
    f(1,2, d=1)

def call3d(f):
    """
    >>> call3d(h)
    Traceback (most recent call last):
    TypeError: h() needs keyword-only argument c
    """
    f(1,2,3, d=1)

def call2cd(f):
    """
    >>> call2cd(f)
    1 2 1 2
    >>> call2cd(m)
    Traceback (most recent call last):
    TypeError: m() got an unexpected keyword argument 'd'
    """
    f(1,2, c=1, d=2)

def call2ce(f):
    """
    >>> call2ce(f)
    Traceback (most recent call last):
    TypeError: f() got an unexpected keyword argument 'e'
    """
    f(1,2, c=1, e=2)

def call2cde(f):
    """
    >>> call2cde(e)
    1 2 1 [('d', 2), ('e', 3)]
    """
    f(1,2, c=1, d=2, e=3)

def call2cf(f):
    """
    >>> call2cf(g)
    1 2 1 42 17 2 []
    >>> call2cf(h)
    1 2 1 42 17 2 () []
    >>> call2cf(k)
    1 2 1 42 17 2 () []
    """
    f(1,2, c=1, f=2)

def call6cf(f):
    """
    >>> call6cf(h)
    1 2 1 42 17 2 (3, 4, 5, 6) []
    """
    f(1,2,3,4,5,6, c=1, f=2)

def call6df(f):
    """
    >>> call6df(k)
    1 2 3 1 17 2 (4, 5, 6) []
    """
    f(1,2,3,4,5,6, d=1, f=2)

def call2cfe(f):
    """
    >>> call2cfe(h)
    1 2 1 42 3 2 () []
    >>> call2cfe(k)
    1 2 1 42 3 2 () []
    """
    f(1,2, c=1, f=2, e=3)

def call2cefd(f):
    """
    >>> call2cefd(g)
    1 2 1 11 0 2 []
    """
    f(1,2, c=1, e=0, f=2, d=11)

def call2cfex(f):
    """
    >>> call2cfex(g)
    1 2 1 42 0 2 [('x', 25)]
    """
    f(1,2, c=1, f=2, e=0, x=25)

def call6argscfexy(f):
    args = (1,2,3,4,5,6)
    f(*args, c=1, f=2, e=3, x=25, y=11)

def call6cfexy(f):
    """
    >>> call6cfexy(h)
    1 2 1 42 3 2 (3, 4, 5, 6) [('x', 25), ('y', 11)]
    """
    f(1,2,3,4,5,6, c=1, f=2, e=3, x=25, y=11)

def call6dfexy(f):
    """
    >>> call6dfexy(k)
    1 2 3 1 3 2 (4, 5, 6) [('x', 25), ('y', 11)]
    """
    f(1,2,3,4,5,6, d=1, f=2, e=3, x=25, y=11)

# the called functions:

def b(a, b, c):
    print a,b,c

def c(a, b, c=1):
    print a,b,c

def d(a, b, *, c = 88):
    print a,b,c

def e(a, b, c = 88, **kwds):
    kwlist = list(kwds.items())
    kwlist.sort()
    print a,b,c, kwlist

def f(a, b, *, c, d = 42):
    print a,b,c,d

def g(a, b, *, c, d = 42, e = 17, f, **kwds):
    kwlist = list(kwds.items())
    kwlist.sort()
    print a,b,c,d,e,f, kwlist

def h(a, b, *args, c, d = 42, e = 17, f, **kwds):
    kwlist = list(kwds.items())
    kwlist.sort()
    print a,b,c,d,e,f, args, kwlist

def k(a, b, c=1, *args, d = 42, e = 17, f, **kwds):
    kwlist = list(kwds.items())
    kwlist.sort()
    print a,b,c,d,e,f, args, kwlist

def m(a, b=1, *, c):
    print a,b,c
