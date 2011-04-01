# ticket: 372

cimport cython

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_modify():
    """
    >>> test_modify()
    0
    1
    2
    3
    4
    <BLANKLINE>
    (4, 0)
    """
    cdef int i, n = 5
    for i in range(n):
        print i
        n = 0
    print
    return i,n

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_negindex():
    """
    >>> test_negindex()
    6
    5
    4
    3
    2
    (2, 0)
    """
    cdef int i, n = 5
    for i in range(n+1, 1, -1):
        print i
        n = 0
    return i,n

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//PrintStatNode//CoerceToPyTypeNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_negindex_inferred():
    """
    >>> test_negindex_inferred()
    5
    4
    3
    2
    (2, 0)
    """
    cdef int n = 5
    for i in range(n, 1, -1):
        print i
        n = 0
    return i,n

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_fix():
    """
    >>> test_fix()
    0
    1
    2
    3
    4
    <BLANKLINE>
    4
    """
    cdef int i
    for i in range(5):
        print i
    print
    return i

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_break():
    """
    >>> test_break()
    0
    1
    2
    <BLANKLINE>
    (2, 0)
    """
    cdef int i, n = 5
    for i in range(n):
        print i
        n = 0
        if i == 2:
            break
    else:
        print "FAILED!"
    print
    return i,n

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_return():
    """
    >>> test_return()
    0
    1
    2
    (2, 0)
    """
    cdef int i, n = 5
    for i in range(n):
        print i
        n = 0
        if i == 2:
            return i,n
    print
    return "FAILED!"
