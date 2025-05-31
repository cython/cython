# mode: run

cimport cython


def slice1(stop):
    """
    >>> list(range(8))
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> list(range(10))[slice1(8)]
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> slice1(1)
    slice(None, 1, None)
    >>> slice1(10)
    slice(None, 10, None)
    >>> slice1(None)
    slice(None, None, None)
    >>> slice1(1) == slice(1)
    True
    >>> slice1(None) == slice(None)
    True
    """
    return slice(stop)


def slice1_const():
    """
    >>> slice1_const() == slice(12)
    True
    """
    return slice(12)


def slice2(start, stop):
    """
    >>> list(range(2, 8))
    [2, 3, 4, 5, 6, 7]
    >>> list(range(10))[slice2(2, 8)]
    [2, 3, 4, 5, 6, 7]
    >>> slice2(1, 10)
    slice(1, 10, None)
    >>> slice2(None, 10)
    slice(None, 10, None)
    >>> slice2(4, None)
    slice(4, None, None)
    """
    return slice(start, stop)


def slice2_const():
    """
    >>> slice2_const() == slice(None, 12)
    True
    """
    return slice(None, 12)


def slice3(start, stop, step):
    """
    >>> list(range(2, 8, 3))
    [2, 5]
    >>> list(range(10))[slice3(2, 8, 3)]
    [2, 5]
    >>> slice3(2, None, 3)
    slice(2, None, 3)
    >>> slice3(None, 3, 2)
    slice(None, 3, 2)
    """
    return slice(start, stop, step)


def slice3_const():
    """
    >>> slice3_const() == slice(12, None, 34)
    True
    """
    return slice(12, None, 34)


def unbound_method_lookup():
    """
    >>> unbound_method_lookup()
    """
    ignore = slice.indices


# BuiltinProperty ends up as a simple call node
@cython.test_assert_path_exists('//SingleAssignmentNode//SimpleCallNode//NameNode[@name="start"]')
@cython.test_fail_if_path_exists('//SingleAssignmentNode//AttributeNode[@is_py_attr = True]')
def typed_slice():
    """
    >>> typed_slice()
    (1, 2, 3)
    """
    cdef slice s
    cdef object z
    cdef Py_ssize_t a,b,c

    z = slice
    s = slice(1, 2, 3)
    s.indices

    a = s.start
    b = s.stop
    c = s.step

    return (a,b,c)


@cython.test_fail_if_path_exists('//SingleAssignmentNode//AttributeNode[@is_py_attr = False]')
def plain_object_slice():
    """
    >>> plain_object_slice()
    (1, 2, 3)
    """
    cdef object s
    cdef object z
    cdef Py_ssize_t a,b,c

    s = slice(1, 2, 3)
    s.indices

    a = s.start
    b = s.stop
    c = s.step

    return (a,b,c)
