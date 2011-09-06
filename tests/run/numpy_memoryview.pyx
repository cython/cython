# tag: numpy
# mode: run

"""
Test slicing for memoryviews and memoryviewslices
"""

cimport numpy as np
import numpy as np

include "cythonarrayutil.pxi"

ctypedef np.int32_t dtype_t

def get_array():
    # We need to type our array to get a __pyx_get_buffer() that typechecks
    # for np.ndarray and calls __getbuffer__ in numpy.pxd
    cdef np.ndarray[dtype_t, ndim=3] a
    a = np.arange(8 * 14 * 11, dtype=np.int32).reshape(8, 14, 11)
    return a

a = get_array()

def ae(*args):
    "assert equals"
    for x in args:
        if x != args[0]:
            raise AssertionError(args)

#
### Test slicing memoryview slices
#

def test_partial_slicing(array):
    """
    >>> test_partial_slicing(a)
    """
    cdef dtype_t[:, :, :] a = array
    obj = array[4]

    cdef dtype_t[:, :] b = a[4, :]
    cdef dtype_t[:, :] c = a[4]

    ae(b.shape[0], c.shape[0], obj.shape[0])
    ae(b.shape[1], c.shape[1], obj.shape[1])
    ae(b.strides[0], c.strides[0], obj.strides[0])
    ae(b.strides[1], c.strides[1], obj.strides[1])

def test_ellipsis(array):
    """
    >>> test_ellipsis(a)
    """
    cdef dtype_t[:, :, :] a = array

    cdef dtype_t[:, :] b = a[..., 4]
    b_obj = array[..., 4]

    cdef dtype_t[:, :] c = a[4, ...]
    c_obj = array[4, ...]

    cdef dtype_t[:, :] d = a[2:8, ..., 2]
    d_obj = array[2:8, ..., 2]

    ae(tuple([b.shape[i] for i in range(2)]), b_obj.shape)
    ae(tuple([b.strides[i] for i in range(2)]), b_obj.strides)
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            ae(b[i, j], b_obj[i, j])

    ae(tuple([c.shape[i] for i in range(2)]), c_obj.shape)
    ae(tuple([c.strides[i] for i in range(2)]), c_obj.strides)
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            ae(c[i, j], c_obj[i, j])

    ae(tuple([d.shape[i] for i in range(2)]), d_obj.shape)
    ae(tuple([d.strides[i] for i in range(2)]), d_obj.strides)
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            ae(d[i, j], d_obj[i, j])

    cdef dtype_t[:] e = a[..., 5, 6]
    e_obj = array[..., 5, 6]
    ae(e.shape[0], e_obj.shape[0])
    ae(e.strides[0], e_obj.strides[0])

#
### Test slicing memoryview objects
#

def test_partial_slicing_memoryview(array):
    """
    >>> test_partial_slicing_memoryview(a)
    """
    cdef dtype_t[:, :, :] _a = array
    a = _a
    obj = array[4]

    b = a[4, :]
    c = a[4]

    ae(b.shape[0], c.shape[0], obj.shape[0])
    ae(b.shape[1], c.shape[1], obj.shape[1])
    ae(b.strides[0], c.strides[0], obj.strides[0])
    ae(b.strides[1], c.strides[1], obj.strides[1])

def test_ellipsis_memoryview(array):
    """
    >>> test_ellipsis_memoryview(a)
    """
    cdef dtype_t[:, :, :] _a = array
    a = _a

    b = a[..., 4]
    b_obj = array[..., 4]

    c = a[4, ...]
    c_obj = array[4, ...]

    d = a[2:8, ..., 2]
    d_obj = array[2:8, ..., 2]

    ae(tuple([b.shape[i] for i in range(2)]), b_obj.shape)
    ae(tuple([b.strides[i] for i in range(2)]), b_obj.strides)
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            ae(b[i, j], b_obj[i, j])

    ae(tuple([c.shape[i] for i in range(2)]), c_obj.shape)
    ae(tuple([c.strides[i] for i in range(2)]), c_obj.strides)
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            ae(c[i, j], c_obj[i, j])

    ae(tuple([d.shape[i] for i in range(2)]), d_obj.shape)
    ae(tuple([d.strides[i] for i in range(2)]), d_obj.strides)
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            ae(d[i, j], d_obj[i, j])

    e = a[..., 5, 6]
    e_obj = array[..., 5, 6]
    ae(e.shape[0], e_obj.shape[0])
    ae(e.strides[0], e_obj.strides[0])

def test_transpose():
    """
    >>> test_transpose()
    3 4
    (3, 4)
    (3, 4)
    11 11 11 11 11 11
    """
    cdef dtype_t[:, :] a

    numpy_obj = np.arange(4 * 3, dtype=np.int32).reshape(4, 3)

    a = numpy_obj
    a_obj = a

    cdef dtype_t[:, :] b = a.T
    print a.T.shape[0], a.T.shape[1]
    print a_obj.T.shape
    print numpy_obj.T.shape

    cdef dtype_t[:, :] c
    with nogil:
        c = a.T.T

    assert (<object> a).shape == (<object> c).shape
    assert (<object> a).strides == (<object> c).strides

    print a[3, 2], a.T[2, 3], a_obj[3, 2], a_obj.T[2, 3], numpy_obj[3, 2], numpy_obj.T[2, 3]

def test_coerce_to_numpy():
    """
    >>> test_coerce_to_numpy()
    34
    34
    2
    """
    cyarray = create_array(shape=(8, 5), mode="c", use_callback=True)
    numarray = np.asarray(cyarray)

    print cyarray[6, 4]
    del cyarray
    print numarray[6, 4]

    numarray[6, 4] = 2
    print numarray[6, 4]

def test_numpy_like_attributes(cyarray):
    """
    >>> cyarray = create_array(shape=(8, 5), mode="c", use_callback=True)
    >>> test_numpy_like_attributes(cyarray)
    >>> test_numpy_like_attributes(cyarray.memview)
    """
    numarray = np.asarray(cyarray)

    assert cyarray.shape == numarray.shape
    assert cyarray.strides == numarray.strides
    assert cyarray.ndim == numarray.ndim
    assert cyarray.size == numarray.size
    assert cyarray.nbytes == numarray.nbytes

    cdef int[:, :] mslice = numarray
    assert (<object> mslice).base is numarray
