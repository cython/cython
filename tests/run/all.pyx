
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

@cython.test_assert_path_exists("//ForInStatNode")
@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//YieldExprNode",
                                 "//GeneratorExpressionNode")
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

@cython.test_assert_path_exists("//ForInStatNode")
@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//YieldExprNode",
                                 "//GeneratorExpressionNode")
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

@cython.test_assert_path_exists("//ForInStatNode")
@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//YieldExprNode",
                                 "//GeneratorExpressionNode")
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
    # FIXME: this isn't really supposed to work, but it currently does
    # due to incorrect scoping - this should be fixed!!
    cdef int x
    return all(x for x in seq)

@cython.test_assert_path_exists("//ForInStatNode")
@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//YieldExprNode",
                                 "//GeneratorExpressionNode")
def all_in_nested_gen(seq):
    """
    >>> all(x for L in [[1,1,1],[1,1,1],[1,1,1]] for x in L)
    True
    >>> all_in_nested_gen([[1,1,1],[1,1,1],[1,1,1]])
    True

    >>> all(x for L in [[1,1,1],[1,1,1],[1,1,0]] for x in L)
    False
    >>> all_in_nested_gen([[1,1,1],[1,1,1],[1,1,0]])
    False

    >>> all(x for L in [[1,1,1],[0,1,1],[1,1,1]] for x in L)
    False
    >>> all_in_nested_gen([[1,1,1],[0,1,1],[1,1,1]])
    False

    >>> all_in_nested_gen([VerboseGetItem([1,1,1]), VerboseGetItem([1,1,1,1,1])])
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
    >>> all_in_nested_gen([VerboseGetItem([1,1,1]),VerboseGetItem([1,1]),VerboseGetItem([1,1,0])])
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
    """
    # FIXME: this isn't really supposed to work, but it currently does
    # due to incorrect scoping - this should be fixed!!
    cdef int x
    return all(x for L in seq for x in L)
