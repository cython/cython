import cython

@cython.locals(a=cython.long, b=cython.long, n=cython.longlong)
def foo(a, b, x, y):
    n = a * b
    # ...
