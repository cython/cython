# mode: run
# tag: all, builtins, werror

cdef class VerboseGetItem(object):
    cdef object sequence
    def __init__(self, seq):
        self.sequence = seq
    def __getitem__(self, i):
        print i
        return self.sequence[i] # may raise IndexError


cimport cython

@cython.test_assert_path_exists(
    "//PyMethodCallNode",
)
@cython.test_fail_if_path_exists(
    "//ForInStatNode",
    "//SimpleCallNode",
)
def all_item(x):
    """
    >>> all_item([1,1,1,1,1])
    True
    >>> all_item([1,1,1,1,0])
    False
    >>> all_item([0,1,1,1,0])
    False

    >>> all(VerboseGetItem([1,1,1,0,0]))
    0
    1
    2
    3
    False
    >>> all_item(VerboseGetItem([1,1,1,0,0]))
    0
    1
    2
    3
    False

    >>> all(VerboseGetItem([1,1,1,1,1]))
    0
    1
    2
    3
    4
    5
    True
    >>> all_item(VerboseGetItem([1,1,1,1,1]))
    0
    1
    2
    3
    4
    5
    True
    """
    return all(x)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PyMethodCallNode",
    "//YieldExprNode",
)
def all_in_simple_gen(seq):
    """
    >>> all_in_simple_gen([1,1,1])
    True
    >>> all_in_simple_gen([1,1,0])
    False
    >>> all_in_simple_gen([1,0,1])
    False

    >>> all_in_simple_gen(VerboseGetItem([1,1,1,1,1]))
    0
    1
    2
    3
    4
    5
    True
    >>> all_in_simple_gen(VerboseGetItem([1,1,0,1,1]))
    0
    1
    2
    False
    """
    return all(x for x in seq)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PyMethodCallNode",
    "//YieldExprNode",
)
def all_in_simple_gen_scope(seq):
    """
    >>> all_in_simple_gen_scope([1,1,1])
    True
    >>> all_in_simple_gen_scope([1,1,0])
    False
    >>> all_in_simple_gen_scope([1,0,1])
    False

    >>> all_in_simple_gen_scope(VerboseGetItem([1,1,1,1,1]))
    0
    1
    2
    3
    4
    5
    True
    >>> all_in_simple_gen_scope(VerboseGetItem([1,1,0,1,1]))
    0
    1
    2
    False
    """
    x = 'abc'
    result = all(x for x in seq)
    assert x == 'abc'
    return result


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PyMethodCallNode",
    "//YieldExprNode",
)
def all_in_conditional_gen(seq):
    """
    >>> all_in_conditional_gen([3,6,9])
    False
    >>> all_in_conditional_gen([0,3,7])
    False
    >>> all_in_conditional_gen([1,0,1])
    True

    >>> all_in_conditional_gen(VerboseGetItem([1,1,1,1,1]))
    0
    1
    2
    3
    4
    5
    True
    >>> all_in_conditional_gen(VerboseGetItem([1,1,0,1,1]))
    0
    1
    2
    3
    4
    5
    True
    """
    return all(x%3 for x in seq if x%2 == 1)


mixed_ustring = u'AbcDefGhIjKlmnoP'
lower_ustring = mixed_ustring.lower()
upper_ustring = mixed_ustring.upper()


@cython.test_assert_path_exists(
    '//PythonCapiCallNode',
    '//ForFromStatNode',
)
@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    "//PyMethodCallNode",
    '//ForInStatNode',
)
def all_lower_case_characters(unicode ustring):
    """
    >>> all_lower_case_characters(mixed_ustring)
    False
    >>> all_lower_case_characters(upper_ustring)
    False
    >>> all_lower_case_characters(lower_ustring)
    True
    """
    return all(uchar.islower() for uchar in ustring)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
    "//InlinedGeneratorExpressionNode//IfStatNode",
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PyMethodCallNode",
    "//YieldExprNode",
#    "//IfStatNode//CoerceToBooleanNode"
)
def all_in_typed_gen(seq):
    """
    >>> all_in_typed_gen([1,1,1])
    True
    >>> all_in_typed_gen([1,0,0])
    False

    >>> all_in_typed_gen(VerboseGetItem([1,1,1,1,1]))
    0
    1
    2
    3
    4
    5
    True
    >>> all_in_typed_gen(VerboseGetItem([1,1,1,1,0]))
    0
    1
    2
    3
    4
    False
    """
    cdef int x
    return all(x for x in seq)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
    "//InlinedGeneratorExpressionNode//IfStatNode",
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PyMethodCallNode",
    "//YieldExprNode",
#    "//IfStatNode//CoerceToBooleanNode"
)
def all_in_double_gen(seq):
    """
    >>> all(x for L in [[1,1,1],[1,1,1],[1,1,1]] for x in L)
    True
    >>> all_in_double_gen([[1,1,1],[1,1,1],[1,1,1]])
    True

    >>> all(x for L in [[1,1,1],[1,1,1],[1,1,0]] for x in L)
    False
    >>> all_in_double_gen([[1,1,1],[1,1,1],[1,1,0]])
    False

    >>> all(x for L in [[1,1,1],[0,1,1],[1,1,1]] for x in L)
    False
    >>> all_in_double_gen([[1,1,1],[0,1,1],[1,1,1]])
    False

    >>> all_in_double_gen([VerboseGetItem([1,1,1]), VerboseGetItem([1,1,1,1,1])])
    0
    1
    2
    3
    0
    1
    2
    3
    4
    5
    True
    >>> all_in_double_gen([VerboseGetItem([1,1,1]),VerboseGetItem([1,1]),VerboseGetItem([1,1,0])])
    0
    1
    2
    3
    0
    1
    2
    0
    1
    2
    False
    >>> all_in_double_gen([VerboseGetItem([1,1,1]),VerboseGetItem([1,0,1]),VerboseGetItem([1,1])])
    0
    1
    2
    3
    0
    1
    False
    """
    cdef int x
    return all(x for L in seq for x in L)
