
cimport cython

@cython.test_fail_if_path_exists("//GeneratorExpressionNode",
                                 "//ComprehensionNode//NoneCheckNode")
@cython.test_assert_path_exists("//ComprehensionNode")
def sorted_genexp():
    """
    >>> sorted_genexp()
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    """
    return sorted(i*i for i in range(10,0,-1))

@cython.test_assert_path_exists("//SimpleCallNode//SimpleCallNode")
def sorted_list():
    """
    >>> sorted_list()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    return sorted(list(range(10,0,-1)))
