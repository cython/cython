# mode: run

import sys
from cython.view cimport array
from libc.stdlib cimport malloc, free

def allocated_data_size():
    """
    >>> allocated_data_size()
    True
    """
    cdef array small = array((1,), sizeof(int), 'i')
    cdef array large = array((1024,), sizeof(int), 'i')
    return sys.getsizeof(large) - sys.getsizeof(small) == 1023 * sizeof(int)

def unallocated_data_size():
    """
    >>> unallocated_data_size()
    True
    """
    cdef array small = array((1,), sizeof(int), 'i', allocate_buffer=False)
    cdef array large = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    return sys.getsizeof(large) == sys.getsizeof(small)

def shape_and_stride_size():
    """
    >>> shape_and_stride_size()
    True
    """
    cdef array one = array((1000,), sizeof(int), 'i')
    cdef array three = array((10, 10, 10), sizeof(int), 'i')
    return sys.getsizeof(three) - sys.getsizeof(one) == 4 * sizeof(Py_ssize_t)

def callback_owned_data_size():
    """
    >>> callback_owned_data_size()
    True
    """
    cdef array owned = array((1024,), sizeof(int), 'i')
    cdef array empty = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    owned.callback_free_data = free
    return sys.getsizeof(owned) - sys.getsizeof(empty) == owned.len

def callback_external_data_size():
    """
    >>> callback_external_data_size()
    True
    """
    cdef array external = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    cdef array empty = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    external.data = <char *> malloc(external.len)
    if external.data == NULL:
        raise MemoryError()
    external.callback_free_data = free
    return sys.getsizeof(external) == sys.getsizeof(empty)

def borrowed_data_size():
    """
    >>> borrowed_data_size()
    True
    """
    cdef int[16] data
    cdef array borrowed = <int[:16]> &data[0]
    cdef array empty = array((16,), sizeof(int), 'i', allocate_buffer=False)
    return sys.getsizeof(borrowed) == sys.getsizeof(empty)
