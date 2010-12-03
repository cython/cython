
cimport cython

@cython.test_assert_path_exists('//TupleNode//CoerceToPyTypeNode//AttributeNode')
def complex_attributes():
    """
    >>> complex_attributes()
    (1.0, 2.0)
    """
    cdef complex c = 1+2j
    return (c.real, c.imag)

@cython.test_assert_path_exists('//TupleNode//CoerceToPyTypeNode//AttributeNode')
def complex_attributes_assign():
    """
    >>> complex_attributes_assign()
    (10.0, 20.0)
    """
    cdef complex c = 1+2j
    c.real, c.imag = 10, 20
    return (c.real, c.imag)

@cython.test_assert_path_exists('//TupleNode//CoerceToPyTypeNode//AttributeNode')
def complex_cstruct_assign():
    """
    >>> complex_cstruct_assign()
    (10.0, 20.0)
    """
    cdef complex c = 1+2j
    cval = &c.cval
    cval.real, cval.imag = 10, 20
    return (c.real, c.imag)
