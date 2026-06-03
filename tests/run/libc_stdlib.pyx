# mode: run

from libc.stdlib cimport abs as c_int_abs, qsort as libc_qsort


def libc_int_abs(int x):
    """
    >>> libc_int_abs(5)
    5
    >>> libc_int_abs(-5)
    5
    """
    return c_int_abs(x)


cdef int gt(const void* v1, const void* v2) noexcept nogil:
    return ((<int*>v1)[0] - (<int*>v2)[0])

cdef int lt(const void* v1, const void* v2) noexcept nogil:
    return - gt(v1, v2)

def qsort(values, direction='lt'):
    """
    >>> data = [1, 9, 3, 2, 5]
    >>> qsort(data, 'gt')
    [1, 2, 3, 5, 9]
    >>> qsort(data, 'lt')
    [9, 5, 3, 2, 1]
    """
    cdef int[5] carray = values[:5]
    libc_qsort(carray, 5, sizeof(int), lt if direction == 'lt' else gt)
    return carray
