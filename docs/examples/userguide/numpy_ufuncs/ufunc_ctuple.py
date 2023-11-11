# tag: numpy
import cython

@cython.ufunc
@cython.cfunc
def add_one_add_two(x: cython.int) -> tuple[cython.int, cython.int]:
    return x+1, x+2
