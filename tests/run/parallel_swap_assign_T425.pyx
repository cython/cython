# ticket: 425

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
    """
    >>> swap_py(1,2)
    (1, 2)
    """
    a,a = b,a
    return a,b


cdef class A:
    cdef readonly object x
    cdef readonly object y
    def __init__(self, x, y):
        self.x, self.y = x, y

@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode/CoerceToTempNode",
    "//ParallelAssignmentNode/SingleAssignmentNode/CoerceToTempNode[@use_managed_ref=False]",
    "//ParallelAssignmentNode/SingleAssignmentNode//AttributeNode/NameNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//AttributeNode[@use_managed_ref=False]/NameNode",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode/CoerceToTempNode[@use_managed_ref=True]",
    "//ParallelAssignmentNode/SingleAssignmentNode/AttributeNode[@use_managed_ref=True]",
    )
def swap_attr_values(A a, A b):
    """
    >>> a, b = A(1,2), A(3,4)
    >>> a.x, a.y, b.x, b.y
    (1, 2, 3, 4)
    >>> swap_attr_values(a,b)
    >>> a.x, a.y, b.x, b.y
    (3, 2, 1, 4)
    """
    a.x, a.y, b.x, b.y = a.y, b.x, b.y, a.x # shift by one
    a.x, a.y, b.x, b.y = b.x, b.y, a.x, a.y # shift by two
    a.x, a.y, b.x, b.y = b.y, b.x, a.y, a.x # reverse


cdef class B:
    cdef readonly A a1
    cdef readonly A a2
    def __init__(self, x1, y1, x2, y2):
        self.a1, self.a2 = A(x1, y1), A(x2, y2)

@cython.test_assert_path_exists(
    "//ParallelAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode",
    "//ParallelAssignmentNode/SingleAssignmentNode/CoerceToTempNode",
    "//ParallelAssignmentNode/SingleAssignmentNode/CoerceToTempNode[@use_managed_ref=False]",
    "//ParallelAssignmentNode/SingleAssignmentNode//AttributeNode/NameNode",
    "//ParallelAssignmentNode/SingleAssignmentNode//AttributeNode[@use_managed_ref=False]/NameNode",
    )
@cython.test_fail_if_path_exists(
    "//ParallelAssignmentNode/SingleAssignmentNode/CoerceToTempNode[@use_managed_ref=True]",
    "//ParallelAssignmentNode/SingleAssignmentNode/AttributeNode[@use_managed_ref=True]",
    )
def swap_recursive_attr_values(B a, B b):
    """
    >>> a, b = B(1,2,3,4), B(5,6,7,8)
    >>> a.a1.x, a.a1.y, a.a2.x, a.a2.y
    (1, 2, 3, 4)
    >>> b.a1.x, b.a1.y, b.a2.x, b.a2.y
    (5, 6, 7, 8)
    >>> swap_recursive_attr_values(a,b)
    >>> a.a1.x, a.a1.y, a.a2.x, a.a2.y
    (2, 1, 4, 4)
    >>> b.a1.x, b.a1.y, b.a2.x, b.a2.y
    (6, 5, 8, 8)

    # compatibility test
    >>> class A:
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    >>> class B:
    ...     def __init__(self, x1, y1, x2, y2):
    ...         self.a1, self.a2 = A(x1, y1), A(x2, y2)
    >>> a, b = B(1,2,3,4), B(5,6,7,8)
    >>> a.a1, a.a2 = a.a2, a.a1
    >>> b.a1, b.a2 = b.a2, b.a1
    >>> a.a1, a.a1.x, a.a2.y, a.a2, a.a1.y, a.a2.x = a.a2, a.a2.y, a.a1.x, a.a1, a.a2.x, a.a1.y
    >>> b.a1, b.a1.x, b.a2.y, b.a2, b.a1.y, b.a2.x = b.a2, b.a2.y, b.a1.x, b.a1, b.a2.x, b.a1.y
    >>> a.a1.x, a.a1.y, a.a2.x, a.a2.y
    (2, 1, 4, 4)
    >>> b.a1.x, b.a1.y, b.a2.x, b.a2.y
    (6, 5, 8, 8)
    """
    a.a1, a.a2 = a.a2, a.a1
    b.a1, b.a2 = b.a2, b.a1
    a.a1, a.a1.x, a.a2.y, a.a2, a.a1.y, a.a2.x = a.a2, a.a2.y, a.a1.x, a.a1, a.a2.x, a.a1.y
    b.a1, b.a1.x, b.a2.y, b.a2, b.a1.y, b.a2.x = b.a2, b.a2.y, b.a1.x, b.a1, b.a2.x, b.a1.y


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
