# ticket: t400

cimport cython


@cython.test_fail_if_path_exists("//SingleAssignmentNode//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//PythonCapiCallNode/PythonCapiFunctionNode/@cname = '__Pyx_truncl'",
)
def long_double_to_float_int(long double x):
    """
    >>> long_double_to_float_int(4.1)
    4.0
    >>> long_double_to_float_int(-4.1)
    -4.0
    >>> long_double_to_float_int(4)
    4.0
    """
    cdef float r = int(x)
    return r
