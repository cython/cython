
cimport cython

# min()

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def min3(a,b,c):
    """
    >>> min3(1,2,3)
    1
    >>> min3(2,3,1)
    1
    >>> min3(2,1,3)
    1
    >>> min3(3,1,2)
    1
    >>> min3(3,2,1)
    1
    """
    return min(a,b,c)

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def min3_list(a,b,c):
    """
    >>> min3_list(1,2,3)
    1
    >>> min3_list(2,3,1)
    1
    >>> min3_list(2,1,3)
    1
    >>> min3_list(3,1,2)
    1
    >>> min3_list(3,2,1)
    1
    """
    return min([a,b,c])

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def min3_tuple(a,b,c):
    """
    >>> min3_tuple(1,2,3)
    1
    >>> min3_tuple(2,3,1)
    1
    >>> min3_tuple(2,1,3)
    1
    >>> min3_tuple(3,1,2)
    1
    >>> min3_tuple(3,2,1)
    1
    """
    return min((a,b,c))

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def min3_typed(int a, int b, int c):
    """
    >>> min3_typed(1,2,3)
    1
    >>> min3_typed(2,3,1)
    1
    >>> min3_typed(2,1,3)
    1
    >>> min3_typed(3,1,2)
    1
    >>> min3_typed(3,2,1)
    1
    """
    return min(a,b,c)

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def literal_min3():
    """
    >>> literal_min3()
    (1, 1, 1, 1, 1)
    """
    return min(1,2,3), min(2,1,3), min(2,3,1), min(3,1,2), min(3,2,1)

# max()

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def max3(a,b,c):
    """
    >>> max3(1,2,3)
    3
    >>> max3(2,3,1)
    3
    >>> max3(2,1,3)
    3
    >>> max3(3,1,2)
    3
    >>> max3(3,2,1)
    3
    """
    return max(a,b,c)

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def max3_typed(int a, int b, int c):
    """
    >>> max3_typed(1,2,3)
    3
    >>> max3_typed(2,3,1)
    3
    >>> max3_typed(2,1,3)
    3
    >>> max3_typed(3,1,2)
    3
    >>> max3_typed(3,2,1)
    3
    """
    return max(a,b,c)

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def literal_max3():
    """
    >>> literal_max3()
    (3, 3, 3, 3, 3)
    """
    return max(1,2,3), max(2,1,3), max(2,3,1), max(3,1,2), max(3,2,1)
