import cython


@cython.test_fail_if_path_exists(
    "//CoerceToBooleanNode//CoerceToPyTypeNode",
)
@cython.test_assert_path_exists(
    "//CoerceToBooleanNode",
)
def test():
    """
    >>> test()
    True
    """
    cdef int x = 5
    return bool(x)


@cython.test_fail_if_path_exists(
    "//CoerceToBooleanNode//CoerceToPyTypeNode",
)
@cython.test_assert_path_exists(
    "//CoerceToBooleanNode",
)
def test_bool_and_int():
    """
    >>> test_bool_and_int()
    1
    """
    cdef int x = 5
    cdef int b = bool(x)
    return b
