# mode: run

import sys
from cython.view cimport array
from libc.stdlib cimport malloc, free

def allocated_data_size():
    """
    >>> allocated_data_size()
    """
    cdef array small = array((1,), sizeof(int), 'i')
    cdef array large = array((1024,), sizeof(int), 'i')
    size_difference = sys.getsizeof(large) - sys.getsizeof(small)
    assert size_difference == 1023 * sizeof(int), size_difference / sizeof(int)

def unallocated_data_size():
    """
    >>> unallocated_data_size()
    """
    cdef array small = array((1,), sizeof(int), 'i', allocate_buffer=False)
    cdef array large = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    size_difference = sys.getsizeof(large) - sys.getsizeof(small)
    assert size_difference == 0, size_difference

def shape_and_stride_size():
    """
    >>> shape_and_stride_size()
    """
    cdef array one = array((1000,), sizeof(int), 'i')
    cdef array three = array((10, 10, 10), sizeof(int), 'i')
    size_difference = sys.getsizeof(three) - sys.getsizeof(one)
    assert size_difference == 4 * sizeof(Py_ssize_t), size_difference / sizeof(Py_ssize_t)

def callback_owned_data_size():
    """
    >>> callback_owned_data_size()
    """
    cdef array owned = array((1024,), sizeof(int), 'i')
    cdef array empty = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    owned.callback_free_data = free
    size_difference = sys.getsizeof(owned) - sys.getsizeof(empty)
    assert size_difference == owned.len, size_difference / sizeof(int)

def callback_external_data_size():
    """
    >>> callback_external_data_size()
    """
    cdef array external = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    cdef array empty = array((1024,), sizeof(int), 'i', allocate_buffer=False)
    external.data = <char *> malloc(external.len)
    if external.data == NULL:
        raise MemoryError()
    external.callback_free_data = free
    size_difference = sys.getsizeof(external) - sys.getsizeof(empty)
    assert size_difference == 0, size_difference

def borrowed_data_size():
    """
    >>> borrowed_data_size()
    """
    cdef int[16] data
    cdef array borrowed = <int[:16]> &data[0]
    cdef array empty = array((16,), sizeof(int), 'i', allocate_buffer=False)
    size_difference = sys.getsizeof(borrowed) - sys.getsizeof(empty)
    assert size_difference == 0, size_difference
