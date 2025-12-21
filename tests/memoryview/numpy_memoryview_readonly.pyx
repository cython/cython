# mode: run
# tag: readonly, const, numpy
# ticket: 1772

import numpy as np
cimport cython

def new_array(dtype='float', writeable=True):
    array = np.arange(10, dtype=dtype)
    array.setflags(write=writeable)
    return array

ARRAY = new_array()


cdef getmax(const double[:] x):
    """Example code, should work with both ro and rw memoryviews"""
    cdef double max_val = -float('inf')
    for val in x:
        if val > max_val:
            max_val = val
    return max_val


cdef update_array(double [:] x):
    """Modifying a ro memoryview should raise an error"""
    x[0] = 23.


cdef getconst(const double [:] x):
    """Should accept ro memoryviews"""
    return x[0]


def test_mmview_rw(x):
    """
    >>> test_mmview_rw(ARRAY)
    9.0
    """
    return getmax(x)


def test_mmview_ro(x):
    """
    >>> test_mmview_ro(new_array())
    9.0
    """
    x.setflags(write=False)
    assert x.flags.writeable is False
    return getmax(x)


def test_update_mmview_rw(x):
    """
    >>> float(test_update_mmview_rw(new_array()))
    23.0
    """
    update_array(x)
    return x[0]


def test_update_mmview_ro(x):
    """
    >>> test_update_mmview_ro(new_array())
    0.0
    """
    x.setflags(write=False)
    assert x.flags.writeable is False
    try:
        update_array(x)
    except ValueError: pass
    else:
        assert False, "RO error not raised!"
    return getconst(x)


def test_rw_call_getmax(double[:] x):
    """
    >>> test_rw_call_getmax(new_array())
    23.0
    """
    update_array(x)
    assert getconst(x) == 23
    return getmax(x)


def test_const_mmview_ro(x):
    """
    >>> test_const_mmview_ro(new_array())
    0.0
    """
    x.setflags(write=False)
    assert x.flags.writeable is False
    return getconst(x)


def test_two_views(x):
    """
    >>> test_two_views(new_array())
    23.0
    """
    cdef double[:] rw = x
    cdef const double[:] ro = rw
    rw[0] = 23
    return ro[0]


def test_assign_ro_to_rw(x):
    """
    >>> test_assign_ro_to_rw(new_array())
    2.0
    """
    cdef const double[:] ro = x
    cdef double[:] rw = np.empty_like(ro)
    rw[:] = ro
    return rw[2]


def test_copy():
    """
    >>> test_copy()
    (1.0, 2.0, 1.0, 1.0, 1.0, 2.0)
    """
    cdef const double[:] ro = np.ones(3)
    cdef const double[:] ro2 = ro.copy()
    cdef double[:] rw = ro.copy()
    cdef double[:] rw2 = ro2.copy()
    rw[1] = 2
    rw2[2] = 2
    return rw[0], rw[1], rw[2], rw2[0], rw2[1], rw2[2]


cdef getmax_floating(const cython.floating[:] x):
    """Function with fused type, should work with both ro and rw memoryviews"""
    cdef cython.floating max_val = - float('inf')
    for val in x:
        if val > max_val:
            max_val = val
    return max_val


def test_mmview_const_fused_cdef():
    """Test cdef function with const fused type memory view as argument.

    >>> test_mmview_const_fused_cdef()
    """
    cdef float[:] data_rw = new_array(dtype='float32')
    assert getmax_floating(data_rw) == 9

    cdef const float[:] data_ro = new_array(dtype='float32', writeable=False)
    assert getmax_floating(data_ro) == 9


def test_mmview_const_fused_def(const cython.floating[:] x):
    """Test def function with const fused type memory view as argument.

    With read-write numpy array:

    >>> test_mmview_const_fused_def(new_array('float32', writeable=True))
    0.0
    >>> test_mmview_const_fused_def(new_array('float64', writeable=True))
    0.0

    With read-only numpy array:

    >>> test_mmview_const_fused_def(new_array('float32', writeable=False))
    0.0
    >>> test_mmview_const_fused_def(new_array('float64', writeable=False))
    0.0
    """
    cdef cython.floating result = x[0]
    return result
