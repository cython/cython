import cython

@exceptval(-2, check=True)
@cython.cfunc
def f(x: cython.double) -> cython.double:
    return x ** 2 - x
