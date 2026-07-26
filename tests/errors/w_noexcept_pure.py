# mode: error
# tag: werror

import cython

@cython.cfunc
@cython.exceptval(check=False)
def test_return_object_noexcept(x) -> object:  # Err
    return x

# declared in pxd as noexcept and cdef
def test_return_object_noexcept_in_pxd(x):  # Err
    return x

# declared in pxd as cdef
def test_return_object_in_pxd(x):  # OK
    return x

@cython.cfunc
@cython.exceptval(check=False)
def test_return_str_noexcept() -> str:  # Err
    return 'a'

@cython.cfunc
@cython.exceptval(check=False)
def test_noexcept():  # Err
    pass

@cython.cfunc
def test_implicit_noexcept():  # Ok
    pass

@cython.cfunc
def test_return_object(x) -> object:  # Ok
    return x

@cython.cfunc
def test_return_str() -> str:  # Ok
    return 'a'

_ERRORS = """
6:0: noexcept clause is ignored for function returning Python object
19:0: noexcept clause is ignored for function returning Python object
24:0: noexcept clause is ignored for function returning Python object

# from pxd
1:46: noexcept clause is ignored for function returning Python object
"""
