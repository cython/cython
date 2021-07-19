@cython.cfunc
@cython.inline
def int_min(a: cython.int, b: cython.int) -> cython.int:
    return b if b < a else a
