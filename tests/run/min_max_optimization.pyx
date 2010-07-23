
cimport cython

class loud_list(list):
    def __len__(self):
        print "calling __len__"
        return super(loud_list, self).__len__()

# max()

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



# min()

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
