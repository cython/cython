# tag: numpy


import numpy as np
cimport numpy as np

int64_array = np.ones((3, 2), dtype=np.int64)

def f():
    """
    >>> f()
    ndim 2
    data 1
    shape 3 2
    shape[1] 2
    strides 16 8
    """
    cdef np.ndarray x = int64_array
    cdef int i
    cdef Py_ssize_t j, k
    cdef char *p
    # todo: int * p: 23:13: Cannot assign type 'char *' to 'int *'

    with nogil:
        i = x.ndim
    print 'ndim', i

    with nogil:
        p = x.data
    print 'data', (<np.int64_t*>p)[0]

    with nogil:
        j = x.shape[0]
        k = x.shape[1]
    print 'shape', j, k
    # Check that non-typical uses still work
    cdef np.npy_intp *shape
    with nogil:
        shape = x.shape + 1
    print 'shape[1]', shape[0]

    with nogil:
        j = x.strides[0]
        k = x.strides[1]
    print 'strides', j, k

def test_non_namenode_attribute_access(obj):
    """
    >>> test_non_namenode_attribute_access(int64_array)
    data 1
    """
    # Try casting, resulting in an AttributeNode with a TypeCastNode as object
    # and 'data' as attribute
    print "data", (<np.int64_t *> (<np.ndarray> obj).data)[0]
