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
    """
    cdef short r = int(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_float_float(short x):
    """
    >>> short_to_float_float(4)
    4.0
    """
    cdef float r = float(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_double_float(short x):
    """
    >>> short_to_double_float(4)
    4.0
    """
    cdef double r = float(x)
    return r

@cython.test_assert_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def short_to_double_int(short x):
    """
    >>> short_to_double_int(4)
    4.0
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
    """
    cdef float r = float(x)
    return r

@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//SingleAssignmentNode/TypecastNode")
def double_to_double_float(double x):
    """
    >>> 4.05 < double_to_double_float(4.1) < 4.15
    True
    >>> double_to_double_float(4)
    4.0
    """
    cdef double r = float(x)
    return r

# tests that cannot be optimised

@cython.test_fail_if_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_assert_path_exists("//SimpleCallNode")
def double_to_py_int(double x):
    """
    >>> double_to_py_int(4.1)
    4
    >>> double_to_py_int(4)
    4
    """
    return int(x)

@cython.test_fail_if_path_exists("//SingleAssignmentNode/TypecastNode")
@cython.test_assert_path_exists("//SimpleCallNode")
def double_to_double_int(double x):
    """
    >>> double_to_double_int(4.1)
    4.0
    >>> double_to_double_int(4)
    4.0
    """
    cdef double r = int(x)
    return r
