# tag: numpy

cimport numpy as np
cimport cython

import numpy as py_numpy

__doc__ = u"""

    >>> test_record_subarray()
    
"""

def test_record_subarray():
    cdef np.ndarray x = py_numpy.zeros((2,2),
                                       dtype=[('a', py_numpy.int32),
                                              ('b', py_numpy.float64, (3, 3))])
    cdef np.dtype descr   = x.dtype
    cdef np.dtype a_descr = descr.fields['a'][0]
    cdef np.dtype b_descr = descr.fields['b'][0]

    # Make sure the dtype looks like we expect
    assert descr.fields == {'a': (py_numpy.dtype('int32'), 0),
                            'b': (py_numpy.dtype(('=f8', (3, 3))), 4)}, descr.fields

    # Make sure that HASSUBARRAY is working
    assert not np.PyDataType_HASSUBARRAY(descr)
    assert not np.PyDataType_HASSUBARRAY(a_descr)
    assert np.PyDataType_HASSUBARRAY(b_descr)

    # Make sure the direct field access works
    assert <tuple>b_descr.subarray.shape == (3, 3), <tuple>b_descr.subarray.shape

    # Make sure the safe high-level helper function works
    assert np.PyDataType_SHAPE(descr) == (), np.PyDataType_SHAPE(descr)
    assert np.PyDataType_SHAPE(a_descr) == (), np.PyDataType_SHAPE(a_descr)
    assert np.PyDataType_SHAPE(b_descr) == (3, 3), np.PyDataType_SHAPE(b_descr)
