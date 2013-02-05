cimport cython

cdef cfunc(a,b,c,d):
    return (a,b,c,d)

cpdef cpfunc(a,b,c,d):
    return (a,b,c,d)


sideeffect = []
cdef side_effect(x):
    sideeffect.append(x)
    return x


@cython.test_fail_if_path_exists('//GeneralCallNode')
@cython.test_assert_path_exists('//SimpleCallNode')
def cfunc_all_keywords():
    """
    >>> cfunc_all_keywords()
    (1, 2, 3, 4)
    """
    return cfunc(a=1, b=2, c=3, d=4)


@cython.test_fail_if_path_exists('//GeneralCallNode')
@cython.test_assert_path_exists('//SimpleCallNode')
def cfunc_some_keywords():
    """
    >>> cfunc_some_keywords()
    (1, 2, 3, 4)
    """
    return cfunc(1, 2, c=3, d=4)


'''
@cython.test_fail_if_path_exists('//GeneralCallNode')
@cython.test_assert_path_exists('//SimpleCallNode')
def cfunc_some_keywords_unordered():
    """
    >>> cfunc_some_keywords_unordered()
    (1, 2, 3, 4)
    """
    return cfunc(1, 2, d=4, d=3)

@cython.test_fail_if_path_exists('//GeneralCallNode')
@cython.test_assert_path_exists('//SimpleCallNode')
def cfunc_some_keywords_unordered_sideeffect():
    """
    >>> del sideeffect[:]
    >>> cfunc_some_keywords_unordered_sideeffect()
    (1, 2, 3, 4)
    >>> sideeffect
    [4, 3]
    """
    return cfunc(1, 2, d=side_effect(4), d=side_effect(3))
'''


@cython.test_fail_if_path_exists('//GeneralCallNode')
@cython.test_assert_path_exists('//SimpleCallNode')
def cpfunc_all_keywords():
    """
    >>> cpfunc_all_keywords()
    (1, 2, 3, 4)
    """
    return cpfunc(a=1, b=2, c=3, d=4)


@cython.test_fail_if_path_exists('//GeneralCallNode')
@cython.test_assert_path_exists('//SimpleCallNode')
def cpfunc_some_keywords():
    """
    >>> cpfunc_some_keywords()
    (1, 2, 3, 4)
    """
    return cpfunc(1, 2, c=3, d=4)


#@cython.test_fail_if_path_exists('//GeneralCallNode')
#@cython.test_assert_path_exists('//SimpleCallNode')
def cpfunc_some_keywords_unordered():
    """
    >>> cpfunc_some_keywords_unordered()
    (1, 2, 3, 4)
    """
    return cpfunc(1, 2, d=4, c=3)


#@cython.test_fail_if_path_exists('//GeneralCallNode')
#@cython.test_assert_path_exists('//SimpleCallNode')
def cpfunc_some_keywords_unordered_sideeffect():
    """
    >>> del sideeffect[:]
    >>> cpfunc_some_keywords_unordered_sideeffect()
    (1, 2, 3, 4)
    >>> sideeffect
    [4, 3]
    """
    return cpfunc(1, 2, d=side_effect(4), c=side_effect(3))
