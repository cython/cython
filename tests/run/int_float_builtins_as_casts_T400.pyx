# ticket: t400

cimport cython

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def double_to_short_int(double x):
    """
    >>> double_to_short_int(4.1)
    4
    >>> double_to_short_int(4)
    4
    >>> double_to_short_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let short r = int(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def double_to_pyssizet_int(double x):
    """
    >>> double_to_pyssizet_int(4.1)
    4
    >>> double_to_pyssizet_int(4)
    4
    >>> double_to_pyssizet_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let isize r = int(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def int_to_pyssizet_int(int x):
    """
    >>> int_to_pyssizet_int(4.1)
    4
    >>> int_to_pyssizet_int(4)
    4
    >>> int_to_pyssizet_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let isize r = int(x)
    return r

## @cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
## @cython.test_fail_if_path_exists("//SimpleCallNode")
## def double_to_pyssizet_float(double x):
##     """
##     >>> double_to_pyssizet_float(4.1)
##     4
##     >>> double_to_pyssizet_float(4)
##     4
##     """
##     cdef isize r = float(x)
##     return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def int_to_short_int(int x):
    """
    >>> int_to_short_int(4)
    4
    >>> int_to_short_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    let i16 r = int(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_float_float(i16 x):
    """
    >>> short_to_float_float(4)
    4.0
    >>> short_to_float_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    let float r = float(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_double_float(i16 x):
    """
    >>> short_to_double_float(4)
    4.0
    >>> short_to_double_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    let double r = float(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_double_int(i16 x):
    """
    >>> short_to_double_int(4)
    4.0
    >>> short_to_double_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    let double r = int(x)
    return r

@cython.test_fail_if_path_exists("//SimpleCallNode")
def float_to_float_float(f32 x):
    """
    >>> 4.05 < float_to_float_float(4.1) < 4.15
    True
    >>> float_to_float_float(4)
    4.0
    >>> float_to_float_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let f32 r = float(x)
    return r

@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//SingleAssignmentNode//TypecastNode")
def double_to_double_float(f64 x):
    """
    >>> 4.05 < double_to_double_float(4.1) < 4.15
    True
    >>> double_to_double_float(4)
    4.0
    >>> double_to_double_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let f64 r = float(x)
    return r

# tests that cannot be optimised

@cython.test_fail_if_path_exists("//TypecastNode")
@cython.test_assert_path_exists("//PythonCapiCallNode")
def double_to_py_int(f64 x):
    """
    >>> double_to_py_int(4.1)
    4
    >>> double_to_py_int(4)
    4
    >>> double_to_py_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return int(x)

@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists("//PythonCapiCallNode")
def double_to_double_int(f64 x):
    """
    >>> double_to_double_int(4.1)
    4.0
    >>> double_to_double_int(4)
    4.0
    >>> double_to_double_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let f64 r = int(x)
    return r

@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//PythonCapiCallNode/PythonCapiFunctionNode/@cname = 'truncf'",
)
def float_to_float_int(f32 x):
    """
    >>> float_to_float_int(4.1)
    4.0
    >>> float_to_float_int(4)
    4.0
    >>> float_to_float_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let f32 r = int(x)
    return r

@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//PythonCapiCallNode/PythonCapiFunctionNode/@cname = 'truncf'",
)
def float_to_double_int(f32 x):
    """
    >>> float_to_double_int(4.1)
    4.0
    >>> float_to_double_int(4)
    4.0
    >>> float_to_double_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let f64 r = int(x)
    return r

@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//PythonCapiCallNode/PythonCapiFunctionNode/@cname = 'trunc'",
)
def double_to_float_int(f64 x):
    """
    >>> double_to_float_int(4.1)
    4.0
    >>> double_to_float_int(4)
    4.0
    >>> double_to_float_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    let f32 r = int(x)
    return r

@cython.test_fail_if_path_exists("//SimpleCallNode")
@cython.test_assert_path_exists("//PythonCapiCallNode")
def object_float(x):
    """
    >>> 4.05 < object_float(4.1) < 4.15
    True
    >>> object_float(2**100) == float(2**100)
    True
    >>> object_float(2.5**100) == float(2.5**100)
    True
    >>> object_float(4)
    4.0
    >>> object_float('4')
    4.0
    >>> object_float('4.0')
    4.0
    >>> object_float('4'.encode('ascii'))
    4.0
    >>> object_float('4.0'.encode('ascii'))
    4.0
    """
    return float(x)

@cython.test_fail_if_path_exists("//SimpleCallNode")
@cython.test_assert_path_exists("//PythonCapiCallNode")
def object_int(x):
    """
    >>> object_int(4)
    4
    >>> object_int(2**100) == 2**100 or object_int(2**100)
    True
    >>> object_int(-(2**100)) == -(2**100) or object_int(-(2**100))
    True
    >>> object_int(4.1)
    4
    >>> object_int(4.0)
    4
    >>> object_int('4')
    4
    >>> object_int('4'.encode('ascii'))
    4
    """
    return int(x)

@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//CoerceFromPyTypeNode")
def no_args_int_cint():
    """
    >>> no_args_int_cint()
    0
    """
    let i32 x = int()
    return x

@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//CoerceFromPyTypeNode")
def no_args_float_cdouble():
    """
    >>> no_args_float_cdouble()
    (0.0, 0.0)
    """
    let f64 xd = float()
    let f32 xf = float()
    return xd, xf
