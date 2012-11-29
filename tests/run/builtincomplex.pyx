
from cpython.complex cimport complex

def complex_attributes():
    """
    >>> complex_attributes()
    (1.0, 2.0)
    """
    cdef complex c = 1+2j
    return (c.real, c.imag)

def complex_attributes_assign():
    """
    >>> complex_attributes_assign()
    (10.0, 20.0)
    """
    cdef complex c = 1+2j
    c.cval.real, c.cval.imag = 10, 20
    return (c.real, c.imag)

def complex_cstruct_assign():
    """
    >>> complex_cstruct_assign()
    (10.0, 20.0)
    """
    cdef complex c = 1+2j
    cval = &c.cval
    cval.real, cval.imag = 10, 20
    return (c.real, c.imag)

def complex_coercion():
    """
    >>> complex_coercion()
    (1.0, 2.0, 1.0, 2.0)
    """
    cdef complex py_c = 1+2j
    cdef double complex c_c = py_c
    cdef object py = c_c
    return (c_c.real, c_c.imag, py.real, py.imag)

def complex_arg(complex c):
    """
    >>> complex_arg(1+2j)
    (1.0, 2.0)
    """
    return (c.real, c.imag)

def complex_conjugate_nonsimple_float():
    """
    >>> complex_conjugate_nonsimple_float()
    1.0
    """
    x = float(1.0).conjugate()
    return x

cdef double float_result():
    return 1.0

def complex_conjugate_nonsimple():
    """
    >>> complex_conjugate_nonsimple()
    1.0
    """
    x = float_result().conjugate()
    return x
