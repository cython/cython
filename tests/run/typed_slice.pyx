__doc__ = u"""
    >>> l = [1,2,3,4]

    >>> slice_list(l)
    [2, 3]
    >>> slice_tuple(tuple(l))
    (2, 3)

    >>> l2 = l[:]
    >>> slice_list_assign_list(l2)
    [1, 1, 2, 3, 4, 4]

    >>> l2 = l[:]
    >>> slice_list_assign_tuple(l2)
    [1, 1, 2, 3, 4, 4]

    >>> l2 = l[:]
    >>> slice_list_assign(l2, (1,2,3,4))
    [1, 1, 2, 3, 4, 4]

    >>> l2 = l[:]
    >>> slice_list_assign(l2, dict(zip(l,l)))
    [1, 1, 2, 3, 4, 4]

    >>> print("%s" % slice_charp('abcdefg'))
    bc
    >>> print("%s" % slice_charp_repeat('abcdefg'))
    cd
"""

def slice_list(list l):
    return l[1:3]

def slice_list_copy(list l):
    cdef list retlist = l[1:3]
    return retlist

def slice_tuple(tuple t):
    return t[1:3]

def slice_list_assign_list(list l):
    l[1:3] = [1,2,3,4]
    return l

def slice_list_assign_tuple(list l):
    l[1:3] = (1,2,3,4)
    return l

def slice_list_assign(list l, value):
    l[1:3] = value
    return l


def slice_charp(py_string_arg):
    cdef str py_string = py_string_arg.encode(u'ASCII')
    cdef char* s = py_string
    return s[1:3].decode(u'ASCII')

def slice_charp_repeat(py_string_arg):
    cdef str py_string = py_string_arg.encode(u'ASCII')
    cdef char* s = py_string
    cdef str slice_val = s[1:6]
    s = slice_val
    return s[1:3].decode(u'ASCII')
