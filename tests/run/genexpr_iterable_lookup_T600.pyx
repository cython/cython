# ticket: 600

cimport cython

@cython.test_assert_path_exists('//ComprehensionNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def list_genexpr_iterable_lookup():
    """
    >>> x = (0,1,2,3,4,5)
    >>> [ x*2 for x in x if x % 2 == 0 ]  # leaks in Py2 but finds the right 'x'
    [0, 4, 8]

    >>> list_genexpr_iterable_lookup()
    [0, 4, 8]
    """
    x = (0,1,2,3,4,5)
    result = list( x*2 for x in x if x % 2 == 0 )
    assert x == (0,1,2,3,4,5)
    return result

@cython.test_assert_path_exists('//ComprehensionNode')
@cython.test_fail_if_path_exists('//SingleAssignmentNode//SimpleCallNode')
def genexpr_iterable_in_closure():
    """
    >>> genexpr_iterable_in_closure()
    [0, 4, 8]
    """
    x = 'abc'
    def f():
        return x
    result = list( x*2 for x in x if x % 2 == 0 )
    assert x == 'abc' # don't leak in Py3 code
    assert f() == 'abc' # don't leak in Py3 code
    return result
