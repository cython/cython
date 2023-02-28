import cython

@cython.cfunc
@cython.ufunc
def add_one_add_two(x: cython.int) -> (cython.int, cython.int):
    return x+1, x+2
