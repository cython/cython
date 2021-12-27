import cython

@cython.cfunc
def cube(x: cython.float) -> cython.float:
    return x * x * x
