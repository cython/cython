# tag: cpp

cimport cython

extern from "cpp_references_helper.h":
    fn i32& ref_func(i32&)
    fn i32& except_ref_func "ref_func" (i32&) except +

    cdef i32 ref_var_value
    cdef i32& ref_var

def test_ref_func(i32 x):
    """
    >>> test_ref_func(2)
    2
    >>> test_ref_func(3)
    3
    """
    return ref_func(x)

def test_ref_func_address(i32 x):
    """
    >>> test_ref_func_address(5)
    5
    >>> test_ref_func_address(7)
    7
    """
    let i32* i_ptr = &ref_func(x)
    return i_ptr[0]

def test_except_ref_func_address(i32 x):
    """
    >>> test_except_ref_func_address(5)
    5
    >>> test_except_ref_func_address(7)
    7
    """
    let i32* i_ptr = &except_ref_func(x)
    return i_ptr[0]

def test_ref_var(i32 x):
    """
    >>> test_ref_func(11)
    11
    >>> test_ref_func(13)
    13
    """
    ref_var = x
    return ref_var_value

def test_ref_assign(i32 x):
    """
    >>> test_ref_assign(17)
    17.0
    >>> test_ref_assign(19)
    19.0
    """
    let f64 d = ref_func(x)
    return d

@cython.infer_types(true)
def test_ref_inference(i32 x):
    """
    >>> test_ref_inference(23)
    23
    >>> test_ref_inference(29)
    29
    """
    z = ref_func(x)
    assert cython.typeof(z) == "int", cython.typeof(z)
    return z
