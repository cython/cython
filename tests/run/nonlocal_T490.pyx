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

