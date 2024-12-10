# mode: run
# tag: complex

import cython


def complex_attributes():
    """
    >>> complex_attributes()
    (1.0, 2.0)
    """
    c: complex = 1+2j
    return (c.real, c.imag)


def complex_coercion():
    """
    >>> complex_coercion()
    (1.0, 2.0, 1.0, 2.0)
    """
    py_c: complex = 1+2j
    c_c: cython.doublecomplex = py_c
    py: object = c_c
    return (c_c.real, c_c.imag, py.real, py.imag)


def complex_arg(c: complex):
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


@cython.cfunc
def float_result() -> cython.double:
    return 1.0


def complex_conjugate_nonsimple():
    """
    >>> complex_conjugate_nonsimple()
    1.0
    """
    x = float_result().conjugate()
    return x


def complex_builtin_function(a, b):
    """
    >>> two = complex_builtin_function(1.0, 0.5)
    >>> two == (2+0j)  or  two
    True
    """
    return complex(a) / complex(b)
