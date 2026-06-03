# tag: numpy
import cython

@cython.ufunc
@cython.cfunc
def generic_add_one(x: cython.numeric) -> cython.numeric:
    return x+1
