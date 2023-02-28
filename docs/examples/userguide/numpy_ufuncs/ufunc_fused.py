import cython

@cython.cfunc
@cython.ufunc
def generic_add_one(x: cython.numeric) -> cython.numeric :
    return x+1
