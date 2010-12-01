
cimport cython

## def range_tuple_genexp(int N):
##     """
##     >>> range_tuple_genexp(5)
##     (0, 1, 2, 3, 4)
##     """
##     return tuple(i for i in range(N))


@cython.test_assert_path_exists('//ForFromStatNode',
                                "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//ForInStatNode')
def range_sum(int N):
    """
    >>> sum(range(10))
    45
    >>> range_sum(10)
    45
    """
    result = sum(i for i in range(N))
    return result


@cython.test_assert_path_exists('//ForFromStatNode',
                                "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//CoerceFromPyTypeNode//InlinedGeneratorExpressionNode',
                                 '//ForInStatNode')
def range_sum_typed(int N):
    """
    >>> sum(range(10))
    45
    >>> range_sum_typed(10)
    45
    """
    cdef int result = sum(i for i in range(N))
    return result


@cython.test_assert_path_exists('//ForFromStatNode',
                                "//InlinedGeneratorExpressionNode",
                                "//ReturnStatNode//InlinedGeneratorExpressionNode",
                                "//ReturnStatNode//CoerceToPyTypeNode//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//CoerceFromPyTypeNode//InlinedGeneratorExpressionNode',
                                 '//TypecastNode//InlinedGeneratorExpressionNode',
                                 '//ForInStatNode')
def return_range_sum_cast(int N):
    """
    >>> sum(range(10))
    45
    >>> return_range_sum_cast(10)
    45
    """
    return <int>sum(i for i in range(N))


@cython.test_assert_path_exists('//ForFromStatNode',
                                "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//ForInStatNode')
def return_range_sum(int N):
    """
    >>> sum(range(10))
    45
    >>> return_range_sum(10)
    45
    """
    return sum(i for i in range(N))


@cython.test_assert_path_exists('//ForFromStatNode',
                                "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//ForInStatNode')
def return_range_sum_squares(int N):
    """
    >>> sum([i*i for i in range(10)])
    285
    >>> return_range_sum_squares(10)
    285

    >>> print(sum([i*i for i in range(10000)]))
    333283335000
    >>> print(return_range_sum_squares(10000))
    333283335000
    """
    return sum(i*i for i in range(N))


@cython.test_assert_path_exists('//ForInStatNode',
                                "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode')
def return_sum_squares(seq):
    """
    >>> sum([i*i for i in range(10)])
    285
    >>> return_sum_squares(range(10))
    285

    >>> print(sum([i*i for i in range(10000)]))
    333283335000
    >>> print(return_sum_squares(range(10000)))
    333283335000
    """
    return sum(i*i for i in seq)


@cython.test_assert_path_exists('//ForInStatNode',
                                "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode')
def return_sum_squares_start(seq, int start):
    """
    >>> sum([i*i for i in range(10)], -1)
    284
    >>> return_sum_squares_start(range(10), -1)
    284

    >>> print(sum([i*i for i in range(10000)], 9))
    333283335009
    >>> print(return_sum_squares_start(range(10000), 9))
    333283335009
    """
    return sum((i*i for i in seq), start)


@cython.test_assert_path_exists(
    '//ForInStatNode',
    "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    "//InlinedGeneratorExpressionNode//CoerceToPyTypeNode")
def return_typed_sum_squares_start(seq, int start):
    """
    >>> sum([i*i for i in range(10)], -1)
    284
    >>> return_typed_sum_squares_start(range(10), -1)
    284

    >>> print(sum([i*i for i in range(1000)], 9))
    332833509
    >>> print(return_typed_sum_squares_start(range(1000), 9))
    332833509
    """
    cdef int i
    return <int>sum((i*i for i in seq), start)


@cython.test_assert_path_exists('//ForInStatNode',
                                "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode')
def return_sum_of_listcomp_consts_start(seq, int start):
    """
    >>> sum([1 for i in range(10) if i > 3], -1)
    5
    >>> return_sum_of_listcomp_consts_start(range(10), -1)
    5

    >>> print(sum([1 for i in range(10000) if i > 3], 9))
    10005
    >>> print(return_sum_of_listcomp_consts_start(range(10000), 9))
    10005
    """
    return sum([1 for i in seq if i > 3], start)


@cython.test_assert_path_exists('//ForInStatNode',
                                "//InlinedGeneratorExpressionNode",
                                # the next test is for a deficiency
                                # (see InlinedGeneratorExpressionNode.coerce_to()),
                                # hope this breaks one day
                                "//CoerceFromPyTypeNode//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists('//SimpleCallNode')
def return_typed_sum_of_listcomp_consts_start(seq, int start):
    """
    >>> sum([1 for i in range(10) if i > 3], -1)
    5
    >>> return_typed_sum_of_listcomp_consts_start(range(10), -1)
    5

    >>> print(sum([1 for i in range(10000) if i > 3], 9))
    10005
    >>> print(return_typed_sum_of_listcomp_consts_start(range(10000), 9))
    10005
    """
    return <int>sum([1 for i in seq if i > 3], start)


@cython.test_assert_path_exists(
    '//ForInStatNode',
    "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    "//InlinedGeneratorExpressionNode//CoerceToPyTypeNode")
def return_typed_sum_cond_exp(seq):
    """
    >>> return_typed_sum_cond_exp([1,2,3,4])
    2
    """
    cdef int i
    return <int>sum( 0 if i%2 else 1
                     for i in seq )


@cython.test_assert_path_exists(
    '//ForInStatNode',
    "//InlinedGeneratorExpressionNode")
@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    "//InlinedGeneratorExpressionNode//CoerceToPyTypeNode")
def return_typed_sum_cond_exp_in(seq):
    """
    >>> return_typed_sum_cond_exp_in([1,2,3,4,5,6,7,8,9])
    3
    """
    cdef int i
    return <int>sum( 0 if i%3 in (0,1) else 1
                     for i in seq )
