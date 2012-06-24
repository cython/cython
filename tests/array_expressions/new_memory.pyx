# tag: numpy
# mode: run

include "utils.pxi"

@testcase
def test_overlapping_memory(fused_dtype_t[:] m1, fused_dtype_t[:, :] m2):
    """
    >>> m1, m2 = operands('l')
    >>> m2 = m2[:2]
    >>> test_overlapping_memory(m1, m2)
    >>> m1
    array([0, 0, 1, 2, 3, 4, 5, 6, 7, 8])
    >>> m2
    array([[10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
           [ 0,  2,  4,  6,  8, 10, 12, 14, 16, 18]])
    """
    # test reads after writes
    m2[...] = m2[::-1, :] + m1
    m1[1:] = m1[:-1]

@testcase
def test_allocate_new_memory_simple(fused_dtype_t[:] m):
    """
    >>> test_allocate_new_memory_simple(np.arange(10, dtype=np.longdouble))
    array([ 0.0,  2.0,  4.0,  6.0,  8.0,  10.0,  12.0,  14.0,  16.0,  18.0], dtype=float128)
    >>> test_allocate_new_memory_simple(object_range(10))
    array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18], dtype=object)
    """
    result = m + m
    return np.asarray(result)

@testcase_like(test_allocate_new_memory_simple)
def test_allocate_new_memory_typed(fused_dtype_t[:] m):
    cdef fused_dtype_t[:] result

    result = m + m
    return np.asarray(result)

@testcase_like(test_allocate_new_memory_simple)
def test_allocate_new_memory_expr(fused_dtype_t[:] m):
    return np.asarray(m + m)

cdef fused_dtype_t[:] func(fused_dtype_t[:] m):
    return m

@testcase_like(test_allocate_new_memory_simple)
def test_allocate_new_memory_expr_typed_call(fused_dtype_t[:] m):
    return np.asarray(func(m + m))
