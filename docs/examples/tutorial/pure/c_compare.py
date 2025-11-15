@cython.cfunc
def c_compare(a: cython.int, b: cython.int) -> cython.bint:
    return a == b
