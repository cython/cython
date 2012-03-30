# mode: run
# tag: numpy

__test__ = {}

def testcase(func):
    __test__[func.__name__] = func.__doc__
    return func


cimport cython
from cython.view cimport array

import numpy as np
cimport numpy as np

@testcase
def test_shape_stride_suboffset():
    u'''
    >>> test_shape_stride_suboffset()
    5 7 11
    77 11 1
    -1 -1 -1
    <BLANKLINE>
    5 7 11
    1 5 35
    -1 -1 -1
    <BLANKLINE>
    5 7 11
    77 11 1
    -1 -1 -1
    '''
    cdef char[:,:,:] larr = array((5,7,11), 1, 'b')
    print larr.shape[0], larr.shape[1], larr.shape[2]
    print larr.strides[0], larr.strides[1], larr.strides[2]
    print larr.suboffsets[0], larr.suboffsets[1], larr.suboffsets[2]
    print

    larr = array((5,7,11), 1, 'b', mode='fortran')
    print larr.shape[0], larr.shape[1], larr.shape[2]
    print larr.strides[0], larr.strides[1], larr.strides[2]
    print larr.suboffsets[0], larr.suboffsets[1], larr.suboffsets[2]
    print

    cdef char[:,:,:] c_contig = larr.copy()
    print c_contig.shape[0], c_contig.shape[1], c_contig.shape[2]
    print c_contig.strides[0], c_contig.strides[1], c_contig.strides[2]
    print c_contig.suboffsets[0], c_contig.suboffsets[1], c_contig.suboffsets[2]

@testcase
def test_copy_to():
    u'''
    >>> test_copy_to()
    0 1 2 3 4 5 6 7
    0 1 2 3 4 5 6 7
    0 1 2 3 4 5 6 7
    '''
    cdef int[:, :, :] from_mvs, to_mvs
    from_mvs = np.arange(8, dtype=np.int32).reshape(2,2,2)
    cdef int *from_data = <int *> from_mvs._data
    print ' '.join(str(from_data[i]) for i in range(2*2*2))
    to_mvs = array((2,2,2), sizeof(int), 'i')
    to_mvs[...] = from_mvs

    cdef int *to_data = <int*>to_mvs._data
    print ' '.join(str(from_data[i]) for i in range(2*2*2))
    print ' '.join(str(to_data[i]) for i in range(2*2*2))

@testcase
def test_overlapping_copy():
    """
    >>> test_overlapping_copy()
    """
    cdef int i, array[10]
    for i in range(10):
        array[i] = i

    cdef int[:] slice = array
    slice[...] = slice[::-1]

    for i in range(10):
        assert slice[i] == 10 - 1 - i

@testcase
def test_partly_overlapping():
    """
    >>> test_partly_overlapping()
    """
    cdef int i, array[10]
    for i in range(10):
        array[i] = i

    cdef int[:] slice = array
    cdef int[:] slice2 = slice[:5]
    slice2[...] = slice[4:9]

    for i in range(5):
        assert slice2[i] == i + 4

@testcase
@cython.nonecheck(True)
def test_nonecheck1():
    u'''
    >>> test_nonecheck1()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    cdef int[:,:,:] uninitialized
    print uninitialized.is_c_contig()

@testcase
@cython.nonecheck(True)
def test_nonecheck2():
    u'''
    >>> test_nonecheck2()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    cdef int[:,:,:] uninitialized
    print uninitialized.is_f_contig()

@testcase
@cython.nonecheck(True)
def test_nonecheck3():
    u'''
    >>> test_nonecheck3()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    cdef int[:,:,:] uninitialized
    uninitialized.copy()

@testcase
@cython.nonecheck(True)
def test_nonecheck4():
    u'''
    >>> test_nonecheck4()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    cdef int[:,:,:] uninitialized
    uninitialized.copy_fortran()

@testcase
@cython.nonecheck(True)
def test_nonecheck5():
    u'''
    >>> test_nonecheck5()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    cdef int[:,:,:] uninitialized
    uninitialized._data

@testcase
def test_copy_mismatch():
    u'''
    >>> test_copy_mismatch()
    Traceback (most recent call last):
       ...
    ValueError: got differing extents in dimension 0 (got 2 and 3)
    '''
    cdef int[:,:,::1] mv1  = array((2,2,3), sizeof(int), 'i')
    cdef int[:,:,::1] mv2  = array((3,2,3), sizeof(int), 'i')

    mv1[...] = mv2

@testcase
def test_is_contiguous():
    u'''
    >>> test_is_contiguous()
    1 1
    0 1
    1 0
    1 0
    <BLANKLINE>
    0 1
    1 0
'''
    cdef int[::1, :, :] fort_contig = array((1,1,1), sizeof(int), 'i', mode='fortran')
    print fort_contig.is_c_contig() , fort_contig.is_f_contig()
    fort_contig = array((200,100,100), sizeof(int), 'i', mode='fortran')
    print fort_contig.is_c_contig(), fort_contig.is_f_contig()
    fort_contig = fort_contig.copy()
    print fort_contig.is_c_contig(), fort_contig.is_f_contig()
    cdef int[:,:,:] strided = fort_contig
    print strided.is_c_contig(), strided.is_f_contig()
    print
    fort_contig = fort_contig.copy_fortran()
    print fort_contig.is_c_contig(), fort_contig.is_f_contig()
    print strided.is_c_contig(), strided.is_f_contig()


@testcase
def call():
    u'''
    >>> call()
    1000 2000 3000
    1000
    2000 3000
    3000
    1 1 1000
    '''
    cdef int[::1] mv1, mv2, mv3
    cdef array arr = array((3,), sizeof(int), 'i')
    mv1 = arr
    cdef int *data
    data = <int*>arr.data
    data[0] = 1000
    data[1] = 2000
    data[2] = 3000

    print (<int*>mv1._data)[0] , (<int*>mv1._data)[1] , (<int*>mv1._data)[2]

    mv2 = mv1.copy()

    print (<int*>mv2._data)[0]


    print (<int*>mv2._data)[1] , (<int*>mv2._data)[2]

    mv3 = mv2

    cdef int *mv3_data = <int*>mv3._data

    print (<int*>mv1._data)[2]

    mv3_data[0] = 1

    print (<int*>mv3._data)[0] , (<int*>mv2._data)[0] , (<int*>mv1._data)[0]

@testcase
def two_dee():
    u'''
    >>> two_dee()
    1 2 3 4
    -4 -4
    1 2 3 -4
    1 2 3 -4
    '''
    cdef long[:,::1] mv1, mv2, mv3
    cdef array arr = array((2,2), sizeof(long), 'l')

    cdef long *arr_data
    arr_data = <long*>arr.data

    mv1 = arr

    arr_data[0] = 1
    arr_data[1] = 2
    arr_data[2] = 3
    arr_data[3] = 4

    print (<long*>mv1._data)[0] , (<long*>mv1._data)[1] , (<long*>mv1._data)[2] , (<long*>mv1._data)[3]

    mv2 = mv1

    arr_data = <long*>mv2._data

    arr_data[3] = -4

    print (<long*>mv2._data)[3] , (<long*>mv1._data)[3]

    mv3 = mv2.copy()

    print (<long*>mv2._data)[0] , (<long*>mv2._data)[1] , (<long*>mv2._data)[2] , (<long*>mv2._data)[3]

    print (<long*>mv3._data)[0] , (<long*>mv3._data)[1] , (<long*>mv3._data)[2] , (<long*>mv3._data)[3]

@testcase
def fort_two_dee():
    u'''
    >>> fort_two_dee()
    1 2 3 4
    -4 -4
    1 2 3 -4
    1 3 2 -4
    1 2 3 -4
    '''
    cdef array arr = array((2,2), sizeof(long), 'l', mode='fortran')
    cdef long[::1,:] mv1, mv2, mv3

    cdef long *arr_data
    arr_data = <long*>arr.data

    mv1 = arr

    arr_data[0] = 1
    arr_data[1] = 2
    arr_data[2] = 3
    arr_data[3] = 4

    print (<long*>mv1._data)[0], (<long*>mv1._data)[1], (<long*>mv1._data)[2], (<long*>mv1._data)[3]

    mv2 = mv1

    arr_data = <long*>mv2._data

    arr_data[3] = -4

    print (<long*>mv2._data)[3], (<long*>mv1._data)[3]

    mv3 = mv2.copy()

    print (<long*>mv2._data)[0], (<long*>mv2._data)[1], (<long*>mv2._data)[2], (<long*>mv2._data)[3]

    print (<long*>mv3._data)[0], (<long*>mv3._data)[1], (<long*>mv3._data)[2], (<long*>mv3._data)[3]

    mv3 = mv3.copy_fortran()

    print (<long*>mv3._data)[0], (<long*>mv3._data)[1], (<long*>mv3._data)[2], (<long*>mv3._data)[3]
