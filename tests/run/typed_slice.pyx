# mode: run
# tag: list, tuple, slice

def slice_list(list l, int start, int stop):
    """
    >>> slice_list([1,2,3,4], 1, 3)
    [2, 3]
    >>> slice_list([1,2,3,4], 1, 7)
    [2, 3, 4]
    >>> slice_list([], 1, 3)
    []
    >>> slice_list([1], 1, 3)
    []
    >>> slice_list([1,2,3,4], -3, -1)
    [2, 3]
    >>> slice_list([1,2,3,4], -10, -1)
    [1, 2, 3]
    >>> slice_list([], -3, -1)
    []
    >>> slice_list([1], -3, -1)
    []
    """
    return l[start:stop]

def slice_list_start(list l, int start):
    """
    >>> slice_list_start([1,2,3,4], 1)
    [2, 3, 4]
    >>> slice_list_start([], 1)
    []
    >>> slice_list_start([1], 1)
    []
    >>> slice_list_start([1], 2)
    []
    >>> slice_list_start([1,2,3,4], -3)
    [2, 3, 4]
    >>> slice_list_start([1,2,3,4], -10)
    [1, 2, 3, 4]
    >>> slice_list_start([], -3)
    []
    >>> slice_list_start([1], -3)
    [1]
    """
    return l[start:]


def slice_list_stop(list l, int stop):
    """
    >>> slice_list_stop([1,2,3,4], 3)
    [1, 2, 3]
    >>> slice_list_stop([1,2,3,4], 7)
    [1, 2, 3, 4]
    >>> slice_list_stop([], 3)
    []
    >>> slice_list_stop([1], 3)
    [1]
    >>> slice_list_stop([1,2,3,4], -3)
    [1]
    >>> slice_list_stop([1,2,3,4], -10)
    []
    >>> slice_list_stop([], -1)
    []
    >>> slice_list_stop([1], -1)
    []
    >>> slice_list_stop([1, 2], -3)
    []
    """
    return l[:stop]


def slice_list_copy(list l):
    """
    >>> slice_list_copy([])
    []
    >>> slice_list_copy([1,2,3])
    [1, 2, 3]
    """
    return l[:]


def slice_tuple_copy(tuple l):
    """
    >>> slice_tuple_copy(())
    ()
    >>> slice_tuple_copy((1,2,3))
    (1, 2, 3)
    """
    return l[:]


def slice_tuple(tuple t, int start, int stop):
    """
    >>> slice_tuple((1,2,3,4), 1, 3)
    (2, 3)
    >>> slice_tuple((1,2,3,4), 1, 7)
    (2, 3, 4)
    >>> slice_tuple((), 1, 3)
    ()
    >>> slice_tuple((1,), 1, 3)
    ()
    >>> slice_tuple((1,2,3,4), -3, -1)
    (2, 3)
    >>> slice_tuple((1,2,3,4), -10, -1)
    (1, 2, 3)
    >>> slice_tuple((), -3, -1)
    ()
    >>> slice_tuple((1,), -3, -1)
    ()
    """
    return t[start:stop]


def slice_tuple_start(tuple t, int start):
    """
    >>> slice_tuple_start((1,2,3,4), 1)
    (2, 3, 4)
    >>> slice_tuple_start((), 1)
    ()
    >>> slice_tuple_start((1,), 1)
    ()
    >>> slice_tuple_start((1,2,3,4), -3)
    (2, 3, 4)
    >>> slice_tuple_start((1,2,3,4), -10)
    (1, 2, 3, 4)
    >>> slice_tuple_start((), -3)
    ()
    >>> slice_tuple_start((1,), -3)
    (1,)
    """
    return t[start:]

def slice_tuple_stop(tuple t, int stop):
    """
    >>> slice_tuple_stop((1,2,3,4), 3)
    (1, 2, 3)
    >>> slice_tuple_stop((1,2,3,4), 7)
    (1, 2, 3, 4)
    >>> slice_tuple_stop((), 3)
    ()
    >>> slice_tuple_stop((1,), 3)
    (1,)
    >>> slice_tuple_stop((1,2,3,4), -1)
    (1, 2, 3)
    >>> slice_tuple_stop((), -1)
    ()
    """
    return t[:stop]


def slice_list_assign_list(list l):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign_list(l2)
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = [1,2,3,4]
    return l


def slice_list_assign_tuple(list l):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign_tuple(l2)
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = (1,2,3,4)
    return l


def slice_list_assign(list l, value):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign(l2, (1,2,3,4))
    [1, 1, 2, 3, 4, 4]
    >>> l2 = l[:]
    >>> slice_list_assign(l2, dict(zip(l,l)))
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = value
    return l


def slice_charp(py_string_arg):
    """
    >>> print("%s" % slice_charp('abcdefg'))
    bc
    """
    cdef bytes py_string = py_string_arg.encode(u'ASCII')
    cdef char* s = py_string
    return s[1:3].decode(u'ASCII')


def slice_charp_repeat(py_string_arg):
    """
    >>> print("%s" % slice_charp_repeat('abcdefg'))
    cd
    """
    cdef bytes py_string = py_string_arg.encode(u'ASCII')
    cdef char* s = py_string
    cdef bytes slice_val = s[1:6]
    s = slice_val
    return s[1:3].decode(u'ASCII')
