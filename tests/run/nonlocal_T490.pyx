def simple():
    """
    >>> simple()
    1
    2
    """
    x = 1
    y = 2
    def f():
        nonlocal x
        nonlocal x, y
        print(x)
        print(y)
    f()

def assign():
    """
    >>> assign()
    1
    """
    xx = 0
    def ff():
        nonlocal xx
        xx += 1
        print(xx)
    ff()

def nested():
    """
    >>> nested()
    1
    """
    x = 0
    def fx():
        def gx():
            nonlocal x
            x=1
            print(x)
        return gx
    fx()()

def arg(x):
    """
    >>> arg('x')
    xyy
    """
    def appendy():
        nonlocal x
        x += 'y'
    x+='y'
    appendy()
    print x
    return

def argtype(int n):
    """
    >>> argtype(0)
    1
    """
    def inc():
        nonlocal n
        n += 1
    inc()
    print n
    return

def ping_pong():
    """
    >>> f = ping_pong()
    >>> inc, dec = f(0)
    >>> inc()
    1
    >>> inc()
    2
    >>> dec()
    1
    >>> inc()
    2
    >>> dec()
    1
    >>> dec()
    0
    """
    def f(x):
        def inc():
            nonlocal x
            x += 1
            return x
        def dec():
            nonlocal x
            x -= 1
            return x
        return inc, dec
    return f

def methods():
    """
    >>> f = methods()
    >>> c = f(0)
    >>> c.inc()
    1
    >>> c.inc()
    2
    >>> c.dec()
    1
    >>> c.dec()
    0
    """
    def f(x):
        class c:
            def inc(self):
                nonlocal x
                x += 1
                return x
            def dec(self):
                nonlocal x
                x -= 1
                return x
        return c()
    return f

# FIXME: doesn't currently work in class namespace:

## def class_body():
##     """
##     >>> c = f(0)
##     >>> c.get()
##     1
##     >>> c.x     #doctest: +ELLIPSIS
##     Traceback (most recent call last):
##     AttributeError: ...
##     """
##     def f(x):
##         class c:
##             nonlocal x
##             x += 1
##             def get(self):
##                 return x
##         return c()

def generator():
    """
    >>> g = generator()
    >>> list(g(5))
    [2, 3, 4, 5, 6]
    """
    def f(x):
        def g(y):
            nonlocal x
            for i in range(y):
                x += 1
                yield x
        return g
    return f(1)

def nested_nonlocals(x):
    """
    >>> g = nested_nonlocals(1)
    >>> h = g()
    >>> h()
    3
    """
    def g():
        nonlocal x
        x -= 2
        def h():
            nonlocal x
            x += 4
            return x
        return h
    return g
