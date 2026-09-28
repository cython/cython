# mode: run
# tag: numpy

cimport numpy as np
import numpy as np


cdef class A(object):
    cdef public int data

    def __init__(self, n):
        self.data = n

## readonly nditer through ndarray of A, summing their data.
def test_readonly():
    """
    >>> test_readonly()
    45
    """

    array_of_A = np.array([A(i) for i in range(10)])

    cdef A scalar_A
    cdef const A[:] chunk
    cdef int total = 0
  
    with np.nditer(array_of_A, flags=['refs_ok', 'external_loop'],
            op_flags=['readonly'], op_dtypes=('object')) as it:

        for chunk in it:
            for i in range(chunk.shape[0]):
                scalar_A = chunk[i]
                total += scalar_A.data

    print total

## readonly nditer through ndarray of A, but modifying the objects
def test_readonly_modify():
    """
    >>> test_readonly_modify()
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    """

    array_of_A = np.array([A(i) for i in range(10)])

    cdef A scalar_A
    cdef const A[:] chunk
    cdef int total = 0
  
    with np.nditer(array_of_A, flags=['refs_ok', 'external_loop'],
            op_flags=['readonly'], op_dtypes=('object')) as it:

        for chunk in it:
            for i in range(chunk.shape[0]):
                scalar_A = chunk[i]
                scalar_A.data *= 2

    print([a.data for a in array_of_A])

# readwrite nditer through ndarray of A, replace objects with twice their data

def test_readwrite():
    """
    >>> test_readwrite()
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    """

    array_of_A = np.array([A(i) for i in range(10)], dtype=A)

    cdef A scalar_A
    cdef A[:] chunk
    cdef int total = 0
  
    with np.nditer(array_of_A, flags=['refs_ok', 'external_loop'],
            op_flags=['readwrite'], op_dtypes=('object')) as it:

        for chunk in it:
            for i in range(chunk.shape[0]):
                scalar_A = chunk[i]
                chunk[i] = A(2 * scalar_A.data)

    print([a.data for a in array_of_A])
    

# 2 operand nditer: Read from first, write to second
def test_readonly_writeonly():
    """
    >>> test_readonly_writeonly()
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    """

    array_in = np.array([A(i) for i in range(10)])
    array_out = np.empty(10, dtype=A)

    cdef A scalar_A
    cdef const A[:] chunk_in
    cdef A[:] chunk_out
    cdef int total = 0
  
    with np.nditer([array_in, array_out], flags=['refs_ok', 'external_loop'],
            op_flags=[['readonly'], ['writeonly']],
            op_dtypes=(A, A)) as it:

        for (chunk_in, chunk_out) in it:
            for i in range(chunk_in.shape[0]):
                scalar_A = chunk_in[i]
                chunk_out[i] = A(2 * scalar_A.data)

    print([a.data for a in array_in])
    print([a.data for a in array_out])
    
