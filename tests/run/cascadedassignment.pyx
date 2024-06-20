import cython

@cython.test_fail_if_path_exists(
    '//CascadedAssignmentNode//CoerceFromPyTypeNode',
    '//CascadedAssignmentNode//CoerceToPyTypeNode',
)
@cython.test_assert_path_exists('//CascadedAssignmentNode')
def test_cascaded_assignment_simple():
    """
    >>> test_cascaded_assignment_simple()
    5
    """
    a = b = c = 5
    return a

@cython.test_fail_if_path_exists(
    '//CascadedAssignmentNode//CoerceFromPyTypeNode',
    '//CascadedAssignmentNode//CoerceToPyTypeNode',
)
@cython.test_assert_path_exists('//CascadedAssignmentNode')
def test_cascaded_assignment_typed():
    """
    >>> test_cascaded_assignment_typed()
    int Python object double
    (5, 5, 5.0)
    """
    cdef int a
    cdef object b
    cdef double c

    a = b = c = 5

    print cython.typeof(a), cython.typeof(b), cython.typeof(c)
    return a, b, c

def test_cascaded_assignment_builtin_expr():
    """
    This test is useful as previously the rhs expr node got replaced resulting
    in CloneNode generating None in the C source.

    >>> test_cascaded_assignment_builtin_expr()
    (10.0, 10.0, 10.0)
    """
    a = b = c = float(10)
    return a, b, c

def expr():
    print "expr called"
    return 10

def test_cascaded_assignment_evaluate_expr():
    """
    >>> test_cascaded_assignment_evaluate_expr()
    expr called
    (10.0, 10.0, 10.0)
    """
    a = b = c = float(expr())
    return a, b, c


def test_overwrite():
    """
    >>> test_overwrite()
    {0: {1: {2: {}}}}
    """
    x = a = {}
    for i in range(3):
        a[i] = a = {}
    assert a == {}
    return x
