with cython.nogil:
    pass  # Placeholder for code intended to run without the GIL

@cython.nogil
@cython.cfunc
@cython.returns(cython.int)
def func_released_gil() -> cython.int:
    return 1