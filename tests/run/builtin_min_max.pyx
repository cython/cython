# mode: run
# tag: optimisation

cimport cython


class loud_list(list):
    def __len__(self):
        print "calling __len__"
        return super(loud_list, self).__len__()


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


@cython.test_assert_path_exists(
    '//PrintStatNode//CondExprNode')
@cython.test_fail_if_path_exists(
    '//PrintStatNode//SimpleCallNode//CoerceToPyTypeNode',
    '//PrintStatNode//SimpleCallNode//ConstNode')
def test_min2():
    """
    >>> test_min2()
    1
    1
    1
    1
    1
    calling __len__
    1
    calling __len__
    1
    """
    cdef int my_int = 1
    cdef object my_pyint = 2
    cdef object my_list = loud_list([1,2,3])

    print min(1, 2)
    print min(2, my_int)
    print min(my_int, 2)

    print min(my_int, my_pyint)
    print min(my_pyint, my_int)

    print min(my_int, len(my_list))
    print min(len(my_list), my_int)


@cython.test_assert_path_exists(
    '//PrintStatNode//CondExprNode')
@cython.test_fail_if_path_exists(
    '//PrintStatNode//SimpleCallNode//CoerceToPyTypeNode',
    '//PrintStatNode//SimpleCallNode//ConstNode')
def test_min3():
    """
    >>> test_min3()
    calling __len__
    1
    calling __len__
    calling __len__
    2
    """
    cdef int my_int = 1
    cdef object my_pyint = 2
    cdef object my_list = loud_list([1,2,3])

    print min(my_int, my_pyint, len(my_list))
    print min(my_pyint, my_list.__len__(), len(my_list))


@cython.test_assert_path_exists(
    '//PrintStatNode//CondExprNode')
@cython.test_fail_if_path_exists(
    '//PrintStatNode//SimpleCallNode//CoerceToPyTypeNode',
    '//PrintStatNode//SimpleCallNode//ConstNode')
def test_minN():
    """
    >>> test_minN()
    calling __len__
    0
    calling __len__
    0
    calling __len__
    0
    """
    cdef int my_int = 1
    cdef object my_pyint = 2
    cdef object my_list = loud_list([1,2,3])

    print min(my_int, 2, my_int, 0, my_pyint, my_int, len(my_list))
    print min(my_int, my_int, 0, my_pyint, my_int, len(my_list))
    print min(my_int, my_int, 2, my_int, 0, my_pyint, my_int, len(my_list))


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


def max1(x):
    """
    >>> max1([1, 2, 3])
    3
    >>> max1([2])
    2
    """
    return max(x)


@cython.test_assert_path_exists(
    '//PrintStatNode//CondExprNode')
@cython.test_fail_if_path_exists(
    '//PrintStatNode//SimpleCallNode//CoerceToPyTypeNode',
    '//PrintStatNode//SimpleCallNode//ConstNode')
def test_max2():
    """
    >>> test_max2()
    2
    2
    2
    2
    2
    calling __len__
    3
    calling __len__
    3
    """
    cdef int my_int = 1
    cdef object my_pyint = 2
    cdef object my_list = loud_list([1,2,3])

    print max(1, 2)
    print max(2, my_int)
    print max(my_int, 2)

    print max(my_int, my_pyint)
    print max(my_pyint, my_int)

    print max(my_int, len(my_list))
    print max(len(my_list), my_int)


@cython.test_assert_path_exists(
    '//PrintStatNode//CondExprNode')
@cython.test_fail_if_path_exists(
    '//PrintStatNode//SimpleCallNode//CoerceToPyTypeNode',
    '//PrintStatNode//SimpleCallNode//ConstNode')
def test_max3():
    """
    >>> test_max3()
    calling __len__
    3
    calling __len__
    calling __len__
    3
    """
    cdef int my_int = 1
    cdef object my_pyint = 2
    cdef object my_list = loud_list([1,2,3])

    print max(my_int, my_pyint, len(my_list))
    print max(my_pyint, my_list.__len__(), len(my_list))


@cython.test_assert_path_exists(
    '//PrintStatNode//CondExprNode')
@cython.test_fail_if_path_exists(
    '//PrintStatNode//SimpleCallNode//CoerceToPyTypeNode',
    '//PrintStatNode//SimpleCallNode//ConstNode')
def test_maxN():
    """
    >>> test_maxN()
    calling __len__
    3
    calling __len__
    3
    calling __len__
    3
    """
    cdef int my_int = 1
    cdef object my_pyint = 2
    cdef object my_list = loud_list([1,2,3])

    print max(my_int, 2, my_int, 0, my_pyint, my_int, len(my_list))
    print max(my_int, my_int, 0, my_pyint, my_int, len(my_list))
    print max(my_int, my_int, 2, my_int, 0, my_pyint, my_int, len(my_list))


'''
# ticket 772
# FIXME: signed vs. unsigned fails to safely handle intermediate results

@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def max3_typed_signed_unsigned(int a, unsigned int b, int c):
    """
    >>> max3_typed_signed_unsigned(1,2,-3)
    2
    >>> max3_typed_signed_unsigned(-2,3,1)
    3
    >>> max3_typed_signed_unsigned(-2,1,-3)
    1
    >>> max3_typed_signed_unsigned(3,-1,2)
    3
    >>> max3_typed_signed_unsigned(-3,2,1)
    2
    """
    return max(a,b,c)
'''
