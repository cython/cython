cdef extern from "cpp_references_helper.h":
    cdef int& ref_func(int&)
    
    cdef int ref_var_value
    cdef int& ref_var

def test_ref_func(int x):
    """
    >>> test_ref_func(2)
    2
    >>> test_ref_func(3)
    3
    """
    return ref_func(x)

def test_ref_func_address(int x):
    """
    >>> test_ref_func_address(5)
    5
    >>> test_ref_func_address(7)
    7
    """
    cdef int* i_ptr = &ref_func(x)
    return i_ptr[0]

def test_ref_var(int x):
    """
    >>> test_ref_func(11)
    11
    >>> test_ref_func(13)
    13
    """
    ref_var = x
    return ref_var_value

def test_ref_assign(int x):
    """
    >>> test_ref_assign(17)
    17.0
    >>> test_ref_assign(19)
    19.0
    """
    cdef double d = ref_func(x)
    return d
