from cython.cimports.libc.math import sin

@cython.cfunc
def f(x: cython.double) -> cython.double:
    return sin(x * x)
