
cdef class VerboseGetItem(object):
    cdef object sequence
    def __init__(self, seq):
        self.sequence = seq
    def __getitem__(self, i):
        print i
        return self.sequence[i] # may raise IndexError


cimport cython

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def any_item(x):
    """
    >>> any_item([0,0,1,0,0])
    True
    >>> any_item([0,0,0,0,1])
    True
    >>> any_item([0,0,0,0,0])
    False

    >>> any(VerboseGetItem([0,0,1,0,0]))
    0
    1
    2
    True
    >>> any_item(VerboseGetItem([0,0,1,0,0]))
    0
    1
    2
    True

    >>> any(VerboseGetItem([0,0,0,0,0]))
    0
    1
    2
    3
    4
    5
    False
    >>> any_item(VerboseGetItem([0,0,0,0,0]))
    0
    1
    2
    3
    4
    5
    False
    """
    return any(x)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode"
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//YieldExprNode"
)
def any_in_simple_gen(seq):
    """
    >>> any_in_simple_gen([0,1,0])
    True
    >>> any_in_simple_gen([0,0,0])
    False

    >>> any_in_simple_gen(VerboseGetItem([0,0,1,0,0]))
    0
    1
    2
    True
    >>> any_in_simple_gen(VerboseGetItem([0,0,0,0,0]))
    0
    1
    2
    3
    4
    5
    False
    """
    return any(x for x in seq)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode"
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//YieldExprNode"
)
def any_in_simple_gen_scope(seq):
    """
    >>> any_in_simple_gen_scope([0,1,0])
    True
    >>> any_in_simple_gen_scope([0,0,0])
    False

    >>> any_in_simple_gen_scope(VerboseGetItem([0,0,1,0,0]))
    0
    1
    2
    True
    >>> any_in_simple_gen_scope(VerboseGetItem([0,0,0,0,0]))
    0
    1
    2
    3
    4
    5
    False
    """
    x = 'abc'
    result = any(x for x in seq)
    assert x == 'abc'
    return result


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode"
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//YieldExprNode"
)
def any_in_conditional_gen(seq):
    """
    >>> any_in_conditional_gen([3,6,9])
    False
    >>> any_in_conditional_gen([0,3,7])
    True
    >>> any_in_conditional_gen([1,0,1])
    True

    >>> any_in_conditional_gen(VerboseGetItem([0,0,3,0,0]))
    0
    1
    2
    3
    4
    5
    False
    >>> any_in_conditional_gen(VerboseGetItem([0,3,0,1,1]))
    0
    1
    2
    3
    True
    """
    return any(x%3 for x in seq if x%2 == 1)

mixed_ustring = u'AbcDefGhIjKlmnoP'
lower_ustring = mixed_ustring.lower()
upper_ustring = mixed_ustring.upper()


@cython.test_assert_path_exists(
    '//PythonCapiCallNode',
    '//ForFromStatNode',
    "//InlinedGeneratorExpressionNode"
)
@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    '//ForInStatNode'
)
def any_lower_case_characters(unicode ustring):
    """
    >>> any_lower_case_characters(upper_ustring)
    False
    >>> any_lower_case_characters(mixed_ustring)
    True
    >>> any_lower_case_characters(lower_ustring)
    True
    """
    return any(uchar.islower() for uchar in ustring)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
    "//InlinedGeneratorExpressionNode//IfStatNode"
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//YieldExprNode",
#    "//IfStatNode//CoerceToBooleanNode"
)
def any_in_typed_gen(seq):
    """
    >>> any_in_typed_gen([0,1,0])
    True
    >>> any_in_typed_gen([0,0,0])
    False

    >>> any_in_typed_gen(VerboseGetItem([0,0,1,0,0]))
    0
    1
    2
    True
    >>> any_in_typed_gen(VerboseGetItem([0,0,0,0,0]))
    0
    1
    2
    3
    4
    5
    False
    """
    cdef int x
    return any(x for x in seq)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
    "//InlinedGeneratorExpressionNode//IfStatNode"
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//YieldExprNode"
)
def any_in_gen_builtin_name(seq):
    """
    >>> any_in_gen_builtin_name([0,1,0])
    True
    >>> any_in_gen_builtin_name([0,0,0])
    False

    >>> any_in_gen_builtin_name(VerboseGetItem([0,0,1,0,0]))
    0
    1
    2
    True
    >>> any_in_gen_builtin_name(VerboseGetItem([0,0,0,0,0]))
    0
    1
    2
    3
    4
    5
    False
    """
    return any(type for type in seq)


@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//InlinedGeneratorExpressionNode",
    "//InlinedGeneratorExpressionNode//IfStatNode"
)
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//YieldExprNode",
#    "//IfStatNode//CoerceToBooleanNode"
)
def any_in_double_gen(seq):
    """
    >>> any(x for L in [[0,0,0],[0,0,1],[0,0,0]] for x in L)
    True
    >>> any_in_double_gen([[0,0,0],[0,0,1],[0,0,0]])
    True

    >>> any(x for L in [[0,0,0],[0,0,0],[0,0,0]] for x in L)
    False
    >>> any_in_double_gen([[0,0,0],[0,0,0],[0,0,0]])
    False

    >>> any_in_double_gen([VerboseGetItem([0,0,0]), VerboseGetItem([0,0,1,0,0])])
    0
    1
    2
    3
    0
    1
    2
    True
    >>> any_in_double_gen([VerboseGetItem([0,0,0]),VerboseGetItem([0,0]),VerboseGetItem([0,0,0])])
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
    3
    False
    """
    cdef int x
    return any(x for L in seq for x in L)
