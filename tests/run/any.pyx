
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

@cython.test_assert_path_exists("//ForInStatNode")
@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//YieldExprNode",
                                 "//GeneratorExpressionNode")
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

@cython.test_assert_path_exists("//ForInStatNode")
@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//YieldExprNode",
                                 "//GeneratorExpressionNode")
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
    # FIXME: this isn't really supposed to work, but it currently does
    # due to incorrect scoping - this should be fixed!!
    cdef int x
    return any(x for x in seq)

@cython.test_assert_path_exists("//ForInStatNode")
@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//YieldExprNode",
                                 "//GeneratorExpressionNode")
def any_in_nested_gen(seq):
    """
    >>> any(x for L in [[0,0,0],[0,0,1],[0,0,0]] for x in L)
    True
    >>> any_in_nested_gen([[0,0,0],[0,0,1],[0,0,0]])
    True

    >>> any(x for L in [[0,0,0],[0,0,0],[0,0,0]] for x in L)
    False
    >>> any_in_nested_gen([[0,0,0],[0,0,0],[0,0,0]])
    False

    >>> any_in_nested_gen([VerboseGetItem([0,0,0]), VerboseGetItem([0,0,1,0,0])])
    0
    1
    2
    3
    0
    1
    2
    True
    >>> any_in_nested_gen([VerboseGetItem([0,0,0]),VerboseGetItem([0,0]),VerboseGetItem([0,0,0])])
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
    # FIXME: this isn't really supposed to work, but it currently does
    # due to incorrect scoping - this should be fixed!!
    cdef int x
    return any(x for L in seq for x in L)
