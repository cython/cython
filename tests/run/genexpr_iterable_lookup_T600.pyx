# mode: run
# ticket: t600
# tag: genexpr
# cython: language_level=3

cimport cython

#@cython.test_assert_path_exists('//ComprehensionNode')
#@cython.test_fail_if_path_exists('//SimpleCallNode')
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


#@cython.test_assert_path_exists('//ComprehensionNode')
#@cython.test_fail_if_path_exists('//SingleAssignmentNode//SimpleCallNode')
def genexpr_iterable_in_closure():
    """
    >>> genexpr_iterable_in_closure()
    ['aa', 'cc']
    """
    x = 'abc'
    def f():
        return x
    result = list( x*2 for x in x if x != 'b' )
    assert x == 'abc' # don't leak in Py3 code
    assert f() == 'abc' # don't leak in Py3 code

    return result


def genexpr_over_complex_arg(func, L):
    """
    >>> class wrapper(object):
    ...     value = 5
    >>> genexpr_over_complex_arg(list, wrapper())
    [5]
    """
    return func(d for d in set([type(L).value, L.__class__.value, L.value]))


def listcomp():
    """
    >>> listcomp()
    [0, 1, 5, 8]
    """
    data = [('red', 5), ('blue', 1), ('yellow', 8), ('black', 0)]
    data.sort(key=lambda r: r[1])
    keys = [r[1] for r in data]
    return keys


def genexpr_in_listcomp(L):
    """
    >>> genexpr_in_listcomp( [[1,2,3]]*2 )
    [[1, 2, 3], [1, 2, 3]]
    """
    return list(d for d in [list(d for d in d) for d in L])


@cython.test_assert_path_exists('//ForFromStatNode')
def genexpr_range_in_listcomp(L):
    """
    >>> genexpr_range_in_listcomp( [1,2,3] )
    [[0], [0, 1], [0, 1, 2]]
    """
    cdef int z,d
    return [list(d for d in range(z)) for z in L]


@cython.test_fail_if_path_exists('//ForInStatNode')
def genexpr_in_dictcomp_dictiter():
    """
    >>> sorted(genexpr_in_dictcomp_dictiter())
    [1, 5]
    """
    d = {1:2, 3:4, 5:6}
    return {k:d for k,d in d.iteritems() if d != 4}


def genexpr_over_array_slice():
    """
    >>> list(genexpr_over_array_slice())
    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    """
    cdef double x[10]
    for i in range(10):
        x[i] = i
    cdef int n = 5
    return (n for n in x[:n+1])
