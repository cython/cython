# mode: error
# ticket: 6009

cimport libc.math as cmath


def f():
    x = cmath.no_such_func()
    return x


def g():
    y = cmath.no_such_const
    return y


_ERRORS = """
8:13: cimported module has no attribute 'no_such_func'
13:13: cimported module has no attribute 'no_such_const'
"""
