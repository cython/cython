# tag: array

import array  # Python builtin module  
from cpython cimport array  # array.pxd / arrayarray.h

a = array.array('f', [1.0, 2.0, 3.0])

def test_len(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> len(a)
    3
    >>> test_len(a)
    3L
    >>> assert len(a) == test_len(a)
    """
    cdef array.array ca = a  # for C-fast array usage
    return ca.length

def test_copy(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_copy(a)
    array('f', [1.0, 2.0, 3.0])
    >>> assert a == test_copy(a)
    """
    cdef array.array ca = a
    cdef array.array b
    b = array.copy(a)
    a[2] = 3.5
    assert b[2] != a[2]
    return b


def test_fast_access(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> a[2]
    3.5

    >>> test_fast_access(a)
    """
    
    cdef array.array ca = a
    assert ca._f[1] == 2.0, ca._f[1]

    assert ca._c[:5] == b'\x00\x00\x80?\x00', ca._c[:5]

    ca._f[1] += 2.0
    assert ca._f[1] == 4.0


def test_new_zero(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_new_zero(a)
    array('f', [0.0, 0.0, 0.0])
    """
    cdef array.array cb = array.clone(a, len(a), True)
    assert cb.length == len(a)
    return cb


def test_set_zero(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_set_zero(a)
    array('f', [0.0, 0.0, 0.0])
    """
    cdef array.array cb = array.copy(a)
    array.zero(cb)
    assert a[1] != 0.0, a
    assert cb[1] == 0.0, cb
    return cb

def test_resize(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_resize(a)
    """
    cdef array.array cb = array.copy(a)
    array.resize(cb, 10)
    for i in range(10):
        cb._f[i] = i
    assert cb.length == 10
    assert cb[9] == cb[-1] == cb._f[9] == 9

def test_view():
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_view()
    """
    a = array.array('i', [1, 2, 3])
    cdef object[int] ca = a
    assert ca[0] == 1
    assert ca[2] == 3

def test_extend():
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_extend()
    """
    cdef array.array ca = array.array('i', [1, 2, 3])
    cdef array.array cb = array.array('i', range(4, 6))
    array.extend(ca, cb)
    assert list(ca) == range(1, 6), list(ca)

def test_likes(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_likes(a)
    array('f', [0.0, 0.0, 0.0])
    """
    cdef array.array z = array.clone(a, len(a), True)
    cdef array.array e = array.clone(a, len(a), False)
    assert e.length == len(a)
    return z

def test_extend_buffer():
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_extend_buffer()
    array('c', 'abcdefghij')
    """
    cdef array.array ca = array.array('c', "abcdef")
    cdef char* s = "ghij"
    array.extend_buffer(ca, s, len(s)) # or use stdlib.strlen

    assert ca._c[9] == 'j'
    assert len(ca) == 10
    return ca
