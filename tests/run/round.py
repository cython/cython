# mode: run

import cython


@cython.cfunc
@cython.returns(cython.float)
def round_float(value: cython.float):
    return round(value)


@cython.cfunc
@cython.returns(cython.double)
def round_double(value: cython.double):
    return round(value)


@cython.cfunc
@cython.returns(cython.longdouble)
def round_long_double(value: cython.longdouble):
    return round(value)


def test_round_float(value):
    """
    >>> test_round_float(3.14)
    3
    >>> test_round_float(0.5)
    0
    >>> test_round_float(1.5)
    2
    >>> test_round_float(-0.5)
    0
    >>> test_round_float(-1.5)
    -2
    """
    return int(round_float(value))


def test_round_double(value):
    """
    >>> test_round_double(3.14)
    3
    >>> test_round_double(0.5)
    0
    >>> test_round_double(1.5)
    2
    >>> test_round_double(-0.5)
    0
    >>> test_round_double(-1.5)
    -2
    """
    return int(round_double(value))


def test_long_double(value):
    """
    >>> test_long_double(3.14)
    3
    >>> test_long_double(0.5)
    0
    >>> test_long_double(1.5)
    2
    >>> test_long_double(-0.5)
    0
    >>> test_long_double(-1.5)
    -2
    """
    return int(round_long_double(value))

<<<<<<< HEAD
=======

>>>>>>> abe1189e2786cd700724d0447eb3af6880e961f4
def test_float_ndigits(value: cython.float, ndigits: cython.int):
    """
    >>> test_float_ndigits(1.25, 0)
   1.0
    >>> test_float_ndigits(1.25, 1)
   1.2 
    >>> test_float_ndigits(1.25, 2)
    1.25
    >>> test_float_ndigits(1.25, 3)
    1.25
    """
<<<<<<< HEAD
    return round(value, ndigits)
=======
    return round(value, ndigits)
>>>>>>> abe1189e2786cd700724d0447eb3af6880e961f4
