# mode: error

def f(*args, **kwargs):
    pass

args   = (1,2,3)
kwargs = {u"test" : "toast"}

def test():
    # ok
    f(1, 2, c=3, *args, d=5, **kwargs, **kwargs)
    f(1, 2, c=3, *args, d=5, **kwargs, x=6)
    f(1, 2, **kwargs, c=3)
    f(1, 2, c=3, *args, *args, **kwargs)
    f(*args, 1, 2, 3)
    # errors
    f(**kwargs, 1, 2, c=3)
    f(*args, **kwargs, *args)
    f(1, 2, c=3, *args, **kwargs, *args)
    f(1=2)


# too bad we don't get more errors here ...

_ERRORS = u"""
17:16: Non-keyword arg following keyword arg
"""
