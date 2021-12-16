#mode: run
#tag: hpy

import cython

@cython.hpy
def add_int_hpy(a:int, b:int):
    """
    >>> add_int_hpy(1, 2)
    3
    """
    return a + b

def add_int_capi(a:int, b:int):
    """
    >>> add_int_capi(1, 2)
    3
    """
    return a + b

assert add_int_hpy(22, 33) == 55
assert add_int_capi(44, 55) == 99
