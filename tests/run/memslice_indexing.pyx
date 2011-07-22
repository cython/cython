cimport cython
from cython cimport array

from libc.stdlib cimport malloc, free

def create_array(shape, mode='c'):
    cdef array result = array(shape, itemsize=sizeof(int), format='i', mode=mode)
    cdef int *data = <int *> result.data
    cdef int i, j, value

    for i in range(shape[0]):
        for j in range(shape[1]):
            value = i * shape[0] + j
            if mode == 'fortran':
                data[i + j * 10] = value
            else:
                data[value] = value

    return result

def slice_contig_indexing():
    """
    >>> slice_contig_indexing()
    98
    61
    98
    61
    """
    cdef int[:, ::1] carr = create_array((14, 10))
    cdef int[::1, :] farr = create_array((10, 14), mode='fortran')

    print carr[9, 8]
    print carr[6, 1]

    print farr[9, 8]
    print farr[6, 1]

