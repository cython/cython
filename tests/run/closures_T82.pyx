__doc__ = u"""
>>> f = add_n(3)
>>> f(2)
5

>>> a(5)()
8

>>> local_x(1)(2)(4)
4 2 1
15

# this currently crashes Cython due to redefinition
#>>> x(1)(2)(4)
#15

>>> x2(1)(2)(4)
15

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

>>> py_twofuncs(1)(2) == cy_twofuncs(1)(2)
True
>>> py_twofuncs(3)(5) == cy_twofuncs(3)(5)
True

>>> inner_funcs = more_inner_funcs(1)(2,4,8)
>>> inner_funcs[0](16), inner_funcs[1](32), inner_funcs[2](64)

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

def local_x(int arg_x):
    cdef int local_x = arg_x
    def y(arg_y):
        y = arg_y
        def z(long arg_z):
            cdef long z = arg_z
            print z, y, local_x
            return 8+z+y+local_x
        return z
    return y

# currently crashes Cython due to name redefinitions (see local_x())
## def x(int x):
##     def y(y):
##         def z(long z):
##             return 8+z+y+x
##         return z
##     return y

def x2(int x2):
    def y2(y2):
        def z2(long z2):
            return 8+z2+y2+x2
        return z2
    return y2


def inner_override(a,b):
    def f():
        a = 1
        return a+b
    return f


def reassign(x):
    def f(a):
        return a+x
    x = 1
    return f

def reassign_int(x):
    def f(int a):
        return a+x
    x = 1
    return f

def reassign_int_int(int x):
    def f(int a):
        return a+x
    x = 1
    return f


def cy_twofuncs(x):
    def f(a):
        return g(x) + a
    def g(b):
        return x + b
    return f


def more_inner_funcs(x):
    def f(a):
        def g(b):
            return a+b+x
        return g
    def g(b):
        def f(a):
            return a+b+x
        return f
    def h(b):
        def f(a):
            return a+b+x
        return f
    def resolve(a_f, b_g, b_h):
        return f(a_f), g(b_g), h(b_h)
    return resolve
