cimport cython

@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'enumerate']")
def go_py_enumerate():
    """
    >>> go_py_enumerate()
    0 1
    1 2
    2 3
    3 4
    """
    for i,k in enumerate(range(1,5)):
        print i, k

@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'enumerate']")
def go_c_enumerate():
    """
    >>> go_c_enumerate()
    0 1
    1 2
    2 3
    3 4
    """
    cdef int i,k
    for i,k in enumerate(range(1,5)):
        print i, k

@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'enumerate']")
def go_c_enumerate_step():
    """
    >>> go_c_enumerate_step()
    0 1
    1 3
    2 5
    """
    cdef int i,k
    for i,k in enumerate(range(1,7,2)):
        print i, k

@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'enumerate']")
def py_enumerate_dict(dict d):
    """
    >>> py_enumerate_dict({})
    :: 55 99
    >>> py_enumerate_dict(dict(a=1, b=2, c=3))
    0 a
    1 c
    2 b
    :: 2 b
    """
    cdef int i = 55
    k = 99
    for i,k in enumerate(d):
        print i, k
    print u"::", i, k

@cython.test_fail_if_path_exists("//SimpleCallNode")
def py_enumerate_break(*t):
    """
    >>> py_enumerate_break(1,2,3,4)
    0 1
    :: 0 1
    """
    i,k = 55,99
    for i,k in enumerate(t):
        print i, k
        break
    print u"::", i, k

@cython.test_fail_if_path_exists("//SimpleCallNode")
def py_enumerate_return(*t):
    """
    >>> py_enumerate_return()
    :: 55 99
    >>> py_enumerate_return(1,2,3,4)
    0 1
    """
    i,k = 55,99
    for i,k in enumerate(t):
        print i, k
        return
    print u"::", i, k

@cython.test_fail_if_path_exists("//SimpleCallNode")
def py_enumerate_continue(*t):
    """
    >>> py_enumerate_continue(1,2,3,4)
    0 1
    1 2
    2 3
    3 4
    :: 3 4
    """
    i,k = 55,99
    for i,k in enumerate(t):
        print i, k
        continue
    print u"::", i, k

@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'enumerate']")
def empty_c_enumerate():
    """
    >>> empty_c_enumerate()
    (55, 99)
    """
    cdef int i = 55, k = 99
    for i,k in enumerate(range(0)):
        print i, k
    return i, k

# not currently optimised
def single_target_enumerate():
    """
    >>> single_target_enumerate()
    0 1
    1 2
    2 3
    3 4
    """
    for t in enumerate(range(1,5)):
        print t[0], t[1]

@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'enumerate']")
def multi_enumerate():
    """
    >>> multi_enumerate()
    0 0 0 1
    1 1 1 2
    2 2 2 3
    3 3 3 4
    """
    for a,(b,(c,d)) in enumerate(enumerate(enumerate(range(1,5)))):
        print a,b,c,d

@cython.test_fail_if_path_exists("//SimpleCallNode")
def multi_c_enumerate():
    """
    >>> multi_c_enumerate()
    0 0 0 1
    1 1 1 2
    2 2 2 3
    3 3 3 4
    """
    cdef int a,b,c,d
    for a,(b,(c,d)) in enumerate(enumerate(enumerate(range(1,5)))):
        print a,b,c,d

@cython.test_fail_if_path_exists("//SimpleCallNode")
def convert_target_enumerate(L):
    """
    >>> convert_target_enumerate([2,3,5])
    0 2
    1 3
    2 5
    """
    cdef int a,b
    for a, b in enumerate(L):
        print a,b
