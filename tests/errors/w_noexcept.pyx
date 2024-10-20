# mode: error
# tag: werror

import cython

ctypedef fused double_or_object:
    double
    object

cdef object test_return_object_noexcept(x) noexcept: # Err
    return x

cdef object test_return_object_noexcept_in_pxd(x) noexcept: # Err
    return x

cdef object test_return_object_in_pxd(x): # OK
    return x

cdef str test_return_str_noexcept() noexcept: # Err
    return 'a'

cdef test_noexcept() noexcept:  # Err
    pass

cdef test_implicit_noexcept(): # Ok
    pass

cdef object test_return_object(x): # Ok
    return x

cdef str test_return_str(): # Ok
    return 'a'

cdef extern from *:
    cdef object extern_return_object(): # Ok
        pass

    cdef object extern_noexcept() noexcept: # Ok
        pass

cdef double_or_object test_fused_noexcept(double_or_object x) noexcept: # Ok
    pass

@cython.exceptval(check=False)
@cython.cfunc
def test_pure_noexcept(): # Err
    pass

@cython.exceptval(check=False)
@cython.cfunc
def test_pure_return_object_noexcept() -> object: # Err
    pass

@cython.exceptval(check=False)
@cython.cfunc
def test_pure_return_str_noexcept() -> str: # Err
    pass

@cython.cfunc
def test_pure_implicit(): # Ok
    pass

@cython.cfunc
def test_pure_return_object() -> object: # Ok
    pass

@cython.cfunc
def test_pure_return_str() -> str: # Ok
    pass

@cython.exceptval(check=False)
@cython.cfunc
def test_pure_return_fused_noexcept(x: double_or_object) -> double_or_object: # Ok
    return x


_ERRORS = """
10:39: noexcept clause is ignored for function returning Python object
13:46: noexcept clause is ignored for function returning Python object
19:33: noexcept clause is ignored for function returning Python object
22:18: noexcept clause is ignored for function returning Python object
44:0: noexcept clause is ignored for function returning Python object
49:0: noexcept clause is ignored for function returning Python object
54:0: noexcept clause is ignored for function returning Python object

# from pxd
1:46: noexcept clause is ignored for function returning Python object
"""
