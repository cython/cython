__doc__ = u"""
>>> test_modify()
0
1
2
3
4
<BLANKLINE>
(4, 0)
>>> test_fix()
0
1
2
3
4
<BLANKLINE>
4
>>> test_break()
0
1
2
<BLANKLINE>
(2, 0)
>>> test_return()
0
1
2
(2, 0)
"""

cimport cython

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_modify():
    cdef int i, n = 5
    for i in range(n):
        print i
        n = 0
    print
    return i,n

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_fix():
    cdef int i
    for i in range(5):
        print i
    print
    return i

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def test_break():
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
    cdef int i, n = 5
    for i in range(n):
        print i
        n = 0
        if i == 2:
            return i,n
    print
    return "FAILED!"
