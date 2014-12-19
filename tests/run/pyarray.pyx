# tag: array

import array  # Python builtin module  
from cpython cimport array  # array.pxd / arrayarray.h

a = array.array('f', [1.0, 2.0, 3.0])

def test_len(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> len(a)
    3
    >>> int(test_len(a))
    3
    >>> assert len(a) == test_len(a)
    """
    cdef array.array ca = a  # for C-fast array usage
    return len(ca)

def test_copy(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_copy(a)
    array('f', [1.0, 2.0, 3.0])
    """
    cdef array.array ca = a
    cdef array.array b
    b = array.copy(ca)
    assert a == b
    a[2] = 3.5
    assert b[2] != a[2]
    return b


def test_fast_access(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_fast_access(a)
    """
    
    cdef array.array ca = a
    
    cdef float value
    with nogil:
        value = ca.data.as_floats[1]
    assert value == 2.0, value

    #assert ca._c[:5] == b'\x00\x00\x80?\x00', repr(ca._c[:5])

    with nogil:
        ca.data.as_floats[1] += 2.0
    assert ca.data.as_floats[1] == 4.0


def test_fast_buffer_access(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_fast_buffer_access(a)
    """
    
    cdef array.array[float] ca = a
    
    cdef float value
    with nogil:
        value = ca[1]
    assert value == 2.0, value

    with nogil:
        ca[1] += 2.0
    assert ca[1] == 4.0


def test_new_zero(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_new_zero(a)
    array('f', [0.0, 0.0, 0.0])
    """
    cdef array.array cb = array.clone(a, len(a), True)
    assert len(cb) == len(a)
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
        cb.data.as_floats[i] = i
    assert len(cb) == 10
    assert cb[9] == cb[-1] == cb.data.as_floats[9] == 9

def test_resize_smart(a):
    """
    >>> a = array.array('d', [1, 2, 3])
    >>> test_resize_smart(a)
    2
    """
    cdef array.array cb = array.copy(a)
    array.resize_smart(cb, 2)
    return len(cb)

def test_buffer():
    """
    >>> test_buffer()
    """
    cdef object a = array.array('i', [1, 2, 3])
    cdef object[int] ca = a
    assert ca[0] == 1
    assert ca[2] == 3

def test_buffer_typed():
    """
    >>> test_buffer_typed()
    """
    cdef array.array a = array.array('i', [1, 2, 3])
    cdef object[int] ca = a
    assert ca[0] == 1
    assert ca[2] == 3

def test_view():
    """
    >>> test_view()
    """
    cdef object a = array.array('i', [1, 2, 3])
    cdef int[:] ca = a
    assert ca[0] == 1
    assert ca[2] == 3

def test_view_typed():
    """
    >>> test_view_typed()
    """
    cdef array.array a = array.array('i', [1, 2, 3])
    cdef int[:] ca = a
    assert ca[0] == 1
    assert ca[2] == 3

def test_extend():
    """
    >>> test_extend()
    """
    cdef array.array ca = array.array('i', [1, 2, 3])
    cdef array.array cb = array.array('i', [4, 5])
    cdef array.array cf = array.array('f', [1.0, 2.0, 3.0])
    array.extend(ca, cb)
    assert list(ca) == [1, 2, 3, 4, 5], list(ca)
    try:
        array.extend(ca, cf)
    except TypeError:
        pass
    else:
        assert False, 'extending incompatible array types did not raise'

def test_likes(a):
    """
    >>> a = array.array('f', [1.0, 2.0, 3.0])
    >>> test_likes(a)
    array('f', [0.0, 0.0, 0.0])
    """
    cdef array.array z = array.clone(a, len(a), True)
    cdef array.array e = array.clone(a, len(a), False)
    assert len(e) == len(a)
    return z

def test_extend_buffer():
    """
    >>> test_extend_buffer()
    array('l', [15, 37, 389, 5077])
    """
    cdef array.array ca = array.array('l', [15, 37])
    cdef long[2] s
    s[0] = 389
    s[1] = 5077
    array.extend_buffer(ca, <char*> &s, 2)

    assert ca.data.as_ulongs[3] == 5077
    assert len(ca) == 4
    return ca
