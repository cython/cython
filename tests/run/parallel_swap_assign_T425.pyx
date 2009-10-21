
cimport cython

@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode/NameNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=False]/NameNode",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=True]",
    )
def swap(a,b):
    """
    >>> swap(1,2)
    (2, 1)
    """
    a,b = b,a
    return a,b


@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode/NameNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=False]/NameNode",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=True]",
    )
def swap5(a,b,c,d,e):
    """
    >>> swap5(1,2,3,4,5)
    (5, 4, 3, 2, 1)
    """
    a,b,c,d,e = e,d,c,b,a
    return a,b,c,d,e


@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode/NameNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=False]/NameNode",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=True]",
    )
cdef bint c_swap_cmp5(a, b, c, d, e):
    a,b,c,d,e = e,d,c,b,a
    return a > b > c > d > e

def swap_cmp5(a,b,c,d,e):
    """
    >>> swap_cmp5(1,2,3,4,5)
    True
    """
    return c_swap_cmp5(a,b,c,d,e)


@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode/NameNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=True]/NameNode",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode//CoerceToTempNode[@use_managed_ref=False]",
    )
def swap_py(a,b):
    a,a = b,a
    return a,b


@cython.test_assert_path_exists(
#    "//ParallelAssignmentNode",
#    "//ParallelAssignmentNode/SingleAssignmentNode",
#    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode",
#    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode[@use_managed_ref=False]",
    )
@cython.test_fail_if_path_exists(
#    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode[@use_managed_ref=True]",
    )
def swap_list_items(list a, int i, int j):
    """
    >>> l = [1,2,3,4]
    >>> swap_list_items(l, 1, 2)
    >>> l
    [1, 3, 2, 4]
    >>> swap_list_items(l, 3, 0)
    >>> l
    [4, 3, 2, 1]
    >>> swap_list_items(l, 0, 5)
    Traceback (most recent call last):
    IndexError: list index out of range
    >>> l
    [4, 3, 2, 1]
    """
    a[i], a[j] = a[j], a[i]


@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode[@use_managed_ref=True]",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode[@use_managed_ref=False]",
    )
def swap_list_items_py1(list a, int i, int j):
    a[i], a[j] = a[j+1], a[i]


@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode[@use_managed_ref=True]",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode//IndexNode[@use_managed_ref=False]",
    )
def swap_list_items_py2(list a, int i, int j):
    a[i], a[j] = a[i], a[i]
