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

    assert descr.fields == {'a': (py_numpy.dtype('int32'), 0),
                            'b': (py_numpy.dtype(('<f8', (3, 3))), 4)}
    assert not np.PyDataType_HASSUBARRAY(descr)
    assert not np.PyDataType_HASSUBARRAY(a_descr)
    assert np.PyDataType_HASSUBARRAY(b_descr)

    assert <tuple>b_descr.subarray.shape == (3, 3)
