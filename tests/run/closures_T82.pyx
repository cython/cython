__doc__ = u"""
>>> f = add_n(3)
>>> f(2)
5

>>> a(5)()
8

# this currently segfaults:
#>>> x(1)(2)(4)
#15

>>> inner_override(2,4)()
5

>>> reassign(4)(2)
3

>>> reassign_int(4)(2)
3

>>> reassign_int_int(4)(2)
3

>>> def py_twofuncs(x):
...    def f(a):
...        return g(x) + a
...    def g(b):
...        return x + b
...    return f

# this currently segfaults:
#>>> py_twofuncs(1)(2) == cy_twofuncs(1)(2)
#True
#>>> py_twofuncs(3)(5) == cy_twofuncs(3)(5)
#True

"""

def add_n(int n):
    def f(int x):
        return x+n
    return f

def a(int x):
    def b():
        def c():
            return 3+x
        return c()
    return b


def x(int x):
    # currently segfaults
    def y(y):
        def z(long z):
            return 8+z+y+x
        return z
    return y


def inner_override(a,b):
    def f():
        a = 1
        return a+b
    return f


def reassign(x):
    def f(a):
        return a+x
    x = 1 # currently lacks a GIVEREF()
    return f

def reassign_int(x):
    def f(int a):
        return a+x
    x = 1 # currently lacks a GIVEREF()
    return f

def reassign_int_int(int x):
    def f(int a):
        return a+x
    x = 1
    return f


def cy_twofuncs(x):
    # pretty ugly segfault
    def f(a):
        return g(x) + a
    def g(b):
        return x + b
    return f
