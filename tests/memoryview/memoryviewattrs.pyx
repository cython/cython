# mode: run
# tag: numpy

cimport cython
from cython.view cimport array

import numpy as np
cimport numpy as np

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
    let char[:, :, :] larr = array((5, 7, 11), 1, 'c')
    print larr.shape[0], larr.shape[1], larr.shape[2]
    print larr.strides[0], larr.strides[1], larr.strides[2]
    print larr.suboffsets[0], larr.suboffsets[1], larr.suboffsets[2]
    print

    larr = array((5, 7, 11), 1, 'c', mode='fortran')
    print larr.shape[0], larr.shape[1], larr.shape[2]
    print larr.strides[0], larr.strides[1], larr.strides[2]
    print larr.suboffsets[0], larr.suboffsets[1], larr.suboffsets[2]
    print

    let char[:, :, :] c_contig = larr.copy()
    print c_contig.shape[0], c_contig.shape[1], c_contig.shape[2]
    print c_contig.strides[0], c_contig.strides[1], c_contig.strides[2]
    print c_contig.suboffsets[0], c_contig.suboffsets[1], c_contig.suboffsets[2]

def test_copy_to():
    u'''
    >>> test_copy_to()
    0 1 2 3 4 5 6 7
    0 1 2 3 4 5 6 7
    0 1 2 3 4 5 6 7
    '''
    let i32[:, :, :] from_mvs, to_mvs
    from_mvs = np.arange(8, dtype=np.int32).reshape(2, 2, 2)

    let i32 *from_data = <i32 *> from_mvs._data
    print ' '.join(str(from_data[i]) for i in range(2 * 2 * 2))

    to_mvs = array((2, 2, 2), sizeof(i32), 'i')
    to_mvs[...] = from_mvs

    # TODO Mark: remove this _data attribute
    let i32 *to_data = <i32*>to_mvs._data
    print ' '.join(str(from_data[i]) for i in range(2 * 2 * 2))
    print ' '.join(str(to_data[i]) for i in range(2 * 2 * 2))

def test_overlapping_copy():
    """
    >>> test_overlapping_copy()
    """
    let i32 i, array[10]
    for i in range(10):
        array[i] = i

    let i32[:] slice = array
    slice[...] = slice[::-1]

    for i in range(10):
        assert slice[i] == 10 - 1 - i

def test_copy_return_type():
    """
    >>> test_copy_return_type()
    60.0
    60.0
    """
    let f64[:, :, :] a = np.arange(5 * 5 * 5, dtype=np.float64).reshape(5, 5, 5)
    let f64[:, ::1] c_contig = a[..., 0].copy()
    let f64[::1, :] f_contig = a[..., 0].copy_fortran()

    print(c_contig[2, 2])
    print(f_contig[2, 2])

def test_partly_overlapping():
    """
    >>> test_partly_overlapping()
    """
    let i32 i, array[10]
    for i in range(10):
        array[i] = i

    let i32[:] slice = array
    let i32[:] slice2 = slice[:5]
    slice2[...] = slice[4:9]

    for i in range(5):
        assert slice2[i] == i + 4

@cython.nonecheck(true)
def test_nonecheck1():
    u'''
    >>> test_nonecheck1()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    let i32[:, :, :] uninitialized
    print uninitialized.is_c_contig()

@cython.nonecheck(true)
def test_nonecheck2():
    u'''
    >>> test_nonecheck2()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    let i32[:, :, :] uninitialized
    print uninitialized.is_f_contig()

@cython.nonecheck(true)
def test_nonecheck3():
    u'''
    >>> test_nonecheck3()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    let i32[:, :, :] uninitialized
    uninitialized.copy()

@cython.nonecheck(true)
def test_nonecheck4():
    u'''
    >>> test_nonecheck4()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    let i32[:, :, :] uninitialized
    uninitialized.copy_fortran()

@cython.nonecheck(true)
def test_nonecheck5():
    u'''
    >>> test_nonecheck5()
    Traceback (most recent call last):
      ...
    UnboundLocalError: local variable 'uninitialized' referenced before assignment
    '''
    let i32[:, :, :] uninitialized
    uninitialized._data

def test_copy_mismatch():
    u'''
    >>> test_copy_mismatch()
    Traceback (most recent call last):
       ...
    ValueError: got differing extents in dimension 0 (got 2 and 3)
    '''
    let i32[:, :, ::1] mv1  = array((2, 2, 3), sizeof(i32), 'i')
    let i32[:, :, ::1] mv2  = array((3, 2, 3), sizeof(i32), 'i')

    mv1[...] = mv2

def test_is_contiguous():
    u"""
    >>> test_is_contiguous()
    one sized is_c/f_contig True True
    is_c/f_contig False True
    f_contig.copy().is_c/f_contig True False
    f_contig.copy_fortran().is_c/f_contig False True
    one sized strided contig True True
    strided False
    """
    let i32[::1, :, :] fort_contig = array((1, 1, 1), sizeof(i32), 'i', mode='fortran')
    let i32[:, :, :] strided = fort_contig

    print 'one sized is_c/f_contig', fort_contig.is_c_contig(), fort_contig.is_f_contig()
    fort_contig = array((2, 2, 2), sizeof(i32), 'i', mode='fortran')
    print 'is_c/f_contig', fort_contig.is_c_contig(), fort_contig.is_f_contig()

    print 'f_contig.copy().is_c/f_contig', fort_contig.copy().is_c_contig(), \
                                           fort_contig.copy().is_f_contig()
    print 'f_contig.copy_fortran().is_c/f_contig', \
           fort_contig.copy_fortran().is_c_contig(), \
           fort_contig.copy_fortran().is_f_contig()

    print 'one sized strided contig', strided.is_c_contig(), strided.is_f_contig()

    print 'strided', strided[::2].is_c_contig()

def call():
    u'''
    >>> call()
    1000 2000 3000
    1000
    2000 3000
    3000
    1 1 1000
    '''
    let i32[::1] mv1, mv2, mv3
    let array arr = array((3,), sizeof(i32), 'i')
    mv1 = arr
    let i32 *data
    data = <i32*>arr.data
    data[0] = 1000
    data[1] = 2000
    data[2] = 3000

    print (<i32*>mv1._data)[0] , (<i32*>mv1._data)[1] , (<i32*>mv1._data)[2]

    mv2 = mv1.copy()

    print (<i32*>mv2._data)[0]


    print (<i32*>mv2._data)[1] , (<i32*>mv2._data)[2]

    mv3 = mv2

    let i32 *mv3_data = <i32*>mv3._data

    print (<i32*>mv1._data)[2]

    mv3_data[0] = 1

    print (<i32*>mv3._data)[0] , (<i32*>mv2._data)[0] , (<i32*>mv1._data)[0]

    assert len(mv1) == 3
    assert len(mv2) == 3
    assert len(mv3) == 3

def two_dee():
    u'''
    >>> two_dee()
    1 2 3 4
    -4 -4
    1 2 3 -4
    1 2 3 -4
    '''
    let i64[:, ::1] mv1, mv2, mv3
    let array arr = array((2, 2), sizeof(i64), 'l')

    assert len(arr) == 2

    try:
        _ = len(mv1)
    except UnboundLocalError:
        pass
    else:
        assert false, "UnboundLocalError not raised for uninitialised memory view"

    let i64 *arr_data
    arr_data = <i64*>arr.data

    mv1 = arr

    arr_data[0] = 1
    arr_data[1] = 2
    arr_data[2] = 3
    arr_data[3] = 4

    print (<i64*>mv1._data)[0] , (<i64*>mv1._data)[1] , (<i64*>mv1._data)[2] , (<i64*>mv1._data)[3]

    mv2 = mv1

    arr_data = <i64*>mv2._data

    arr_data[3] = -4

    print (<i64*>mv2._data)[3] , (<i64*>mv1._data)[3]

    mv3 = mv2.copy()

    print (<i64*>mv2._data)[0] , (<i64*>mv2._data)[1] , (<i64*>mv2._data)[2] , (<i64*>mv2._data)[3]

    print (<i64*>mv3._data)[0] , (<i64*>mv3._data)[1] , (<i64*>mv3._data)[2] , (<i64*>mv3._data)[3]

def fort_two_dee():
    u'''
    >>> fort_two_dee()
    1 2 3 4
    -4 -4
    1 2 3 -4
    1 3 2 -4
    1 2 3 -4
    '''
    let array arr = array((2, 2), sizeof(i64), 'l', mode='fortran')
    let i64[::1, :] mv1, mv2, mv4
    let i64[:, ::1] mv3

    let i64 *arr_data
    arr_data = <i64*>arr.data

    mv1 = arr

    arr_data[0] = 1
    arr_data[1] = 2
    arr_data[2] = 3
    arr_data[3] = 4

    print (<i64*>mv1._data)[0], (<i64*>mv1._data)[1], (<i64*>mv1._data)[2], (<i64*>mv1._data)[3]

    mv2 = mv1

    arr_data = <i64*>mv2._data

    arr_data[3] = -4

    print (<i64*>mv2._data)[3], (<i64*>mv1._data)[3]

    mv3 = mv2.copy()

    print (<i64*>mv2._data)[0], (<i64*>mv2._data)[1], (<i64*>mv2._data)[2], (<i64*>mv2._data)[3]

    print (<i64*>mv3._data)[0], (<i64*>mv3._data)[1], (<i64*>mv3._data)[2], (<i64*>mv3._data)[3]

    mv4 = mv3.copy_fortran()

    print (<i64*>mv4._data)[0], (<i64*>mv4._data)[1], (<i64*>mv4._data)[2], (<i64*>mv4._data)[3]
