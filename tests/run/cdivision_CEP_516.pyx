__doc__ = u"""
>>> v = [(17, 10), (-17, 10), (-17, -10), (17, -10)]
>>> standard = [(a % b) for a, b in v]
>>> standard
[7, 3, -7, -3]
>>> [mod_int_py(a, b) for a, b in v] == standard
True
>>> [mod_short_py(a, b) for a, b in v] == standard
True
>>> [mod_float_py(a, b) for a, b in v] == standard
True
>>> [mod_double_py(a, b) for a, b in v] == standard
True

>>> [mod_int_c(a, b) for a, b in v]
[7, -7, -7, 7]
>>> [mod_float_c(a, b) for a, b in v]
[7.0, -7.0, -7.0, 7.0]
>>> [mod_double_c(a, b) for a, b in v]
[7.0, -7.0, -7.0, 7.0]

>>> [div_int_py(a, b) for a, b in v]
[1, -2, 1, -2]
>>> [div_int_c(a, b) for a, b in v]
[1, -1, 1, -1]

>>> [test_cdiv_cmod(a, b) for a, b in v]
[(1, 7), (-1, -7), (1, -7), (-1, 7)]

>>> [test_cdiv_cmod(a, b) for a, b in [(4, -4), (4, -2), (4, -1)]]
[(-1, 0), (-2, 0), (-4, 0)]

>>> all([mod_int_py(a, b) == a % b for a in range(-10, 10) for b in range(-10, 10) if b != 0])
True
>>> all([div_int_py(a, b) == a // b for a in range(-10, 10) for b in range(-10, 10) if b != 0])
True
"""

import warnings
orig_showwarning = warnings.showwarning

true_py_functions = {}
exec "def simple_warn(msg, *args): print(msg)" in true_py_functions
simple_warn = true_py_functions['simple_warn']
del true_py_functions


def _all(seq):
    for x in seq:
        if not x:
            return false
    return true

try:
    all
except NameError:
    all = _all


cimport cython

@cython.cdivision(false)
def mod_int_py(i32 a, i32 b):
    return a % b

@cython.cdivision(false)
def mod_short_py(i16 a, i16 b):
    return a % b

@cython.cdivision(false)
def mod_double_py(f64 a, f64 b):
    return a % b

@cython.cdivision(false)
def mod_float_py(f32 a, f32 b):
    return a % b

@cython.cdivision(true)
def mod_int_c(i32 a, i32 b):
    return a % b

@cython.cdivision(true)
def mod_float_c(f32 a, f32 b):
    return a % b

@cython.cdivision(true)
def mod_double_c(f64 a, f64 b):
    return a % b

@cython.cdivision(false)
def div_int_py(i32 a, i32 b):
    return a // b

@cython.cdivision(true)
def div_int_c(i32 a, i32 b):
    return a // b

@cython.cdivision(false)
def test_cdiv_cmod(i16 a, i16 b):
    let i16 q = cython.cdiv(a, b)
    let i16 r = cython.cmod(a, b)
    return q, r

@cython.cdivision(true)
@cython.cdivision_warnings(true)
def mod_int_c_warn(i32 a, i32 b):
    """
    >>> warnings.showwarning = simple_warn
    >>> mod_int_c_warn(-17, 10)
    division with oppositely signed operands, C and Python semantics differ
    -7
    >>> warnings.showwarning = orig_showwarning
    """
    return a % b

@cython.cdivision(true)
@cython.cdivision_warnings(true)
def div_int_c_warn(i32 a, i32 b):
    """
    >>> warnings.showwarning = simple_warn
    >>> div_int_c_warn(-17, 10)
    division with oppositely signed operands, C and Python semantics differ
    -1
    >>> warnings.showwarning = orig_showwarning
    """
    return a // b

@cython.cdivision(false)
@cython.cdivision_warnings(true)
def complex_expression(i32 a, i32 b, i32 c, i32 d):
    """
    >>> warnings.showwarning = simple_warn
    >>> complex_expression(-150, 20, 19, -7)
    verbose_call(20)
    division with oppositely signed operands, C and Python semantics differ
    verbose_call(19)
    division with oppositely signed operands, C and Python semantics differ
    -2
    >>> warnings.showwarning = orig_showwarning
    """
    return (a // verbose_call(b)) % (verbose_call(c) // d)

fn i32 verbose_call(i32 x):
    print u"verbose_call(%s)" % x
    return x

# These may segfault with cdivision

@cython.cdivision(false)
def mod_div_zero_int(i32 a, i32 b, i32 c):
    """
    >>> mod_div_zero_int(25, 10, 2)
    verbose_call(5)
    2
    >>> print(mod_div_zero_int(25, 10, 0))
    verbose_call(5)
    integer division or modulo by zero
    >>> print(mod_div_zero_int(25, 0, 0))
    integer division or modulo by zero
    """
    try:
        return verbose_call(a % b) / c
    except ZeroDivisionError, ex:
        return unicode(ex)

@cython.cdivision(false)
def mod_div_zero_float(f32 a, f32 b, f32 c):
    """
    >>> mod_div_zero_float(25, 10, 2)
    2.5
    >>> print(mod_div_zero_float(25, 10, 0))
    float division
    >>> print(mod_div_zero_float(25, 0, 0))
    float divmod()
    """
    try:
        return (a % b) / c
    except ZeroDivisionError, ex:
        return unicode(ex)

@cython.cdivision(false)
def py_div_long(i64 a, i64 b):
    """
    >>> py_div_long(-5, -1)
    5
    >>> import sys
    >>> maxint = getattr(sys, ((sys.version_info[0] >= 3) and 'maxsize' or 'maxint'))
    >>> py_div_long(-maxint-1, -1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...
    """
    return a / b

def c_div_const_test(a, b):
    """
    >>> c_div_const_test(5, 3)
    1
    """
    return c_div_const(a, b)

fn i64 c_div_const(const i64 a, i32 b):
    let i64 c = a / b
    return c
