# tag: numpy
# mode: run

cimport numpy as np
import numpy as np

def test_simple_binop_assign(int[:] m):
    """
    >>> a = np.arange(10, dtype='i')
    >>> np.asarray(test_simple_binop_assign(a))
    array([ 0,  1,  4,  9, 16, 25, 36, 49, 64, 81], dtype=int32)
    """
    m[:] = m * m
    return m

def test_simple_binop_assign_contig(int[::1] m):
    """
    >>> a = np.arange(10, dtype='i')
    >>> np.asarray(test_simple_binop_assign_contig(a))
    array([ 0,  1,  4,  9, 16, 25, 36, 49, 64, 81], dtype=int32)
    """
    m[:] = m * m
    return m

def test_simple_binop_assign_2d(int[:, :] m):
    """
    >>> a2d = np.arange(100, dtype='i').reshape(10, 10)
    >>> np.asarray(test_simple_binop_assign_2d(a2d))
    array([[  0,   3,   6,   9,  12,  15,  18,  21,  24,  27],
           [ 30,  33,  36,  39,  42,  45,  48,  51,  54,  57],
           [ 60,  63,  66,  69,  72,  75,  78,  81,  84,  87],
           [ 90,  93,  96,  99, 102, 105, 108, 111, 114, 117],
           [120, 123, 126, 129, 132, 135, 138, 141, 144, 147],
           [150, 153, 156, 159, 162, 165, 168, 171, 174, 177],
           [180, 183, 186, 189, 192, 195, 198, 201, 204, 207],
           [210, 213, 216, 219, 222, 225, 228, 231, 234, 237],
           [240, 243, 246, 249, 252, 255, 258, 261, 264, 267],
           [270, 273, 276, 279, 282, 285, 288, 291, 294, 297]], dtype=int32)
    """
    m[:] = m + m + m
    return m

def test_simple_binop_assign_contig_2d(int[:, :] m):
    """
    >>> a2d = np.arange(100, dtype='i').reshape(10, 10)
    >>> np.asarray(test_simple_binop_assign_contig_2d(a2d))
    array([[  0,   3,   6,   9,  12,  15,  18,  21,  24,  27],
           [ 30,  33,  36,  39,  42,  45,  48,  51,  54,  57],
           [ 60,  63,  66,  69,  72,  75,  78,  81,  84,  87],
           [ 90,  93,  96,  99, 102, 105, 108, 111, 114, 117],
           [120, 123, 126, 129, 132, 135, 138, 141, 144, 147],
           [150, 153, 156, 159, 162, 165, 168, 171, 174, 177],
           [180, 183, 186, 189, 192, 195, 198, 201, 204, 207],
           [210, 213, 216, 219, 222, 225, 228, 231, 234, 237],
           [240, 243, 246, 249, 252, 255, 258, 261, 264, 267],
           [270, 273, 276, 279, 282, 285, 288, 291, 294, 297]], dtype=int32)
    """
    m[:] = m + m + m
    return m

def test_typedef(np.int32_t[:] m):
    """
    >>> np.asarray(test_typedef(np.arange(10, dtype=np.int32)))
    array([ 0,  3,  6,  9, 12, 15, 18, 21, 24, 27], dtype=int32)
    """
    m[:] = m + m + m
    return m

cdef fused fused_dtype_t:
    long
    long double
    double complex
    object

def test_arbitrary_dtypes(fused_dtype_t[:] m):
    """
    >>> test_arbitrary_dtypes(np.arange(10, dtype='l'))
    array([ 0,  3,  6,  9, 12, 15, 18, 21, 24, 27])
    >>> test_arbitrary_dtypes(np.arange(10, dtype=np.longdouble))
    array([ 0.0,  3.0,  6.0,  9.0,  12.0,  15.0,  18.0,  21.0,  24.0,  27.0], dtype=float128)
    >>> test_arbitrary_dtypes(np.arange(10, dtype=np.complex128) + 1.2j)
    array([  0.+3.6j,   3.+3.6j,   6.+3.6j,   9.+3.6j,  12.+3.6j,  15.+3.6j,
            18.+3.6j,  21.+3.6j,  24.+3.6j,  27.+3.6j])
    >>> test_arbitrary_dtypes(np.arange(10, dtype=np.object))
    array([0, 3, 6, 9, 12, 15, 18, 21, 24, 27], dtype=object)
    """
    m[:] = m + m + m
    return np.asarray(m)
