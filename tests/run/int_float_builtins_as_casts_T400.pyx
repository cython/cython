# ticket: 400

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
    cdef short r = int(x)
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
    cdef Py_ssize_t r = int(x)
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
    cdef Py_ssize_t r = int(x)
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
##     cdef Py_ssize_t r = float(x)
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
    cdef short r = int(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_float_float(short x):
    """
    >>> short_to_float_float(4)
    4.0
    >>> short_to_float_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    cdef float r = float(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_double_float(short x):
    """
    >>> short_to_double_float(4)
    4.0
    >>> short_to_double_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    cdef double r = float(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_double_int(short x):
    """
    >>> short_to_double_int(4)
    4.0
    >>> short_to_double_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    cdef double r = int(x)
    return r

@cython.test_fail_if_path_exists("//SimpleCallNode")
def float_to_float_float(float x):
    """
    >>> 4.05 < float_to_float_float(4.1) < 4.15
    True
    >>> float_to_float_float(4)
    4.0
    >>> float_to_float_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    cdef float r = float(x)
    return r

@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//SingleAssignmentNode//TypecastNode")
def double_to_double_float(double x):
    """
    >>> 4.05 < double_to_double_float(4.1) < 4.15
    True
    >>> double_to_double_float(4)
    4.0
    >>> double_to_double_float('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    cdef double r = float(x)
    return r

# tests that cannot be optimised

@cython.test_fail_if_path_exists("//TypecastNode")
@cython.test_assert_path_exists("//PythonCapiCallNode")
def double_to_py_int(double x):
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
def double_to_double_int(double x):
    """
    >>> double_to_double_int(4.1)
    4.0
    >>> double_to_double_int(4)
    4.0
    >>> double_to_double_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    cdef double r = int(x)
    return r


@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//PythonCapiCallNode/PythonCapiFunctionNode/@cname = 'truncf'",
)
def float_to_float_int(float x):
    """
    >>> float_to_float_int(4.1)
    4.0
    >>> float_to_float_int(4)
    4.0
    >>> float_to_float_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    cdef float r = int(x)
    return r


@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//PythonCapiCallNode/PythonCapiFunctionNode/@cname = 'truncf'",
)
def float_to_double_int(float x):
    """
    >>> float_to_double_int(4.1)
    4.0
    >>> float_to_double_int(4)
    4.0
    >>> float_to_double_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    cdef double r = int(x)
    return r


@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//PythonCapiCallNode/PythonCapiFunctionNode/@cname = 'trunc'",
)
def double_to_float_int(double x):
    """
    >>> double_to_float_int(4.1)
    4.0
    >>> double_to_float_int(4)
    4.0
    >>> double_to_float_int('4')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    cdef float r = int(x)
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
    cdef int x = int()
    return x


@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//CoerceFromPyTypeNode")
def no_args_float_cdouble():
    """
    >>> no_args_float_cdouble()
    (0.0, 0.0)
    """
    cdef double xd = float()
    cdef float xf = float()
    return xd, xf
