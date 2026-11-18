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


def _loud(x):
    print(x)
    return x


@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'max']")
def max_evaluation_order():
    """
    >>> max_evaluation_order()
    1
    2
    3
    3
    """
    print(max(_loud(1), _loud(2), _loud(3)))


@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'min']")
def min_evaluation_order():
    """
    >>> min_evaluation_order()
    3
    2
    1
    1
    """
    print(min([_loud(3), _loud(2), _loud(1)]))


cdef int _loud_int(int x):
    print(x)
    return x


@cython.test_assert_path_exists("//CondExprNode")
def max_evaluation_order_typed():
    """
    >>> max_evaluation_order_typed()
    1
    2
    2
    """
    print(max(_loud_int(1), _loud_int(2)))


class Cmp:
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return f"Cmp({self._value})"

    def __lt__(self, other):
        print(f"{self._value} < {other._value}")
        return self._value < other._value

    def __gt__(self, other):
        print(f"{self._value} > {other._value}")
        return self._value > other._value

    def __eq__(self, other):
        print(f"{self._value} == {other._value}")
        return self._value == other._value


@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'min']")
def min_evaluation_order_cmp():
    """
    >>> print(min([Cmp(4), Cmp(3), Cmp(2), Cmp(1)]))
    3 < 4
    2 < 3
    1 < 2
    Cmp(1)
    >>> min_evaluation_order_cmp()
    3 < 4
    2 < 3
    1 < 2
    Cmp(1)
    """
    print(min([Cmp(4), Cmp(3), Cmp(2), Cmp(1)]))


@cython.test_assert_path_exists("//CondExprNode")
@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'max']")
def max_evaluation_order_cmp():
    """
    >>> print(max([Cmp(4), Cmp(3), Cmp(2), Cmp(1)]))
    3 > 4
    2 > 4
    1 > 4
    Cmp(4)
    >>> max_evaluation_order_cmp()
    3 > 4
    2 > 4
    1 > 4
    Cmp(4)
    """
    print(max([Cmp(4), Cmp(3), Cmp(2), Cmp(1)]))


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
