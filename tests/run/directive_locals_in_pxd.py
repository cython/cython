import cython

# @cython.locals(x=double)
# cdef func_defval(x=0):
    # return x**2

def foo(egg):
    if not cython.compiled:
        egg = float(egg)
    return egg

def test_pxd_locals():
    """
    >>> isinstance(test_pxd_locals(), float)
    True
    """
    return foo(1)
