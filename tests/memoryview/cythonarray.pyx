# mode: run

from __future__ import unicode_literals

# these imports allow testing different ways to access [[cython.]view.]array()
from cython.view cimport array
from cython cimport view as v
cimport cython as cy

include "cythonarrayutil.pxi"


def length(shape):
    """
    >>> len(length((2,)))
    2
    >>> len(length((2,3)))
    2
    >>> len(length((5,3,2)))
    5
    """
    cdef array cvarray = array(shape=shape, itemsize=sizeof(int), format="i", mode='c')
    assert len(cvarray) == shape[0]
    return cvarray


def contiguity():
    '''
    >>> contiguity()
    12 4
    2 3
    2
    <BLANKLINE>
    4 8
    2 3
    2
    '''
    cdef v.array cvarray = cy.view.array(shape=(2,3), itemsize=sizeof(int), format="i", mode='c')
    assert cvarray.len == 2*3*sizeof(int), (cvarray.len, 2*3*sizeof(int))
    assert cvarray.itemsize == sizeof(int)
    print cvarray.strides[0], cvarray.strides[1]
    print cvarray.shape[0], cvarray.shape[1]
    print cvarray.ndim

    print

    cdef v.array farray = v.array(shape=(2,3), itemsize=sizeof(int), format="i", mode='fortran')
    assert farray.len == 2*3*sizeof(int)
    assert farray.itemsize == sizeof(int)
    print farray.strides[0], farray.strides[1]
    print farray.shape[0], farray.shape[1]
    print farray.ndim

def acquire():
    '''
    >>> acquire()
    '''
    cdef object[int, ndim=1, mode="c"] buf1d = \
            array(shape=(10,), itemsize=sizeof(int), format='i', mode='c')
    cdef object[int, ndim=2, mode="c"] buf2d = \
            array(shape=(10,10), itemsize=sizeof(int), format='i')
    cdef object[unsigned long, ndim=3, mode='fortran'] buf3d = \
            array(shape=(1,2,3), itemsize=sizeof(unsigned long), format='L', mode='fortran')
    cdef object[long double, ndim=3, mode='fortran'] bufld = \
            array(shape=(1,2,3), itemsize=sizeof(long double), format='g', mode='fortran')

def full_or_strided():
    '''
    >>> full_or_strided()
    '''
    cdef object[float, ndim=2, mode='full'] fullbuf = \
            array(shape=(10,10), itemsize=sizeof(float), format='f', mode='c')
    cdef object[long long int, ndim=3, mode='strided'] stridedbuf = \
            array(shape=(1,2,3), itemsize=sizeof(long long int), format='q', mode='fortran')

def dont_allocate_buffer():
    """
    >>> dont_allocate_buffer()
    callback called
    """
    cdef array result = array((10, 10), itemsize=sizeof(int), format='i', allocate_buffer=False)
    assert result.data == NULL
    result.callback_free_data = callback
    result = None

def test_cython_array_getbuffer():
    """
    >>> test_cython_array_getbuffer()
    98
    61
    98
    61
    """
    cdef int[:, ::1] cslice = create_array((14, 10), 'c')
    cdef int[::1, :] fslice = create_array((14, 10), 'fortran')

    print cslice[9, 8]
    print cslice[6, 1]

    print fslice[9, 8]
    print fslice[6, 1]

def test_cython_array_index():
    """
    >>> test_cython_array_index()
    98
    61
    98
    61
    """
    c_array = create_array((14, 10), 'c')
    f_array = create_array((14, 10), 'fortran')

    print c_array[9, 8]
    print c_array[6, 1]

    print f_array[9, 8]
    print f_array[6, 1]

cdef int *getp(int dim1=10, int dim2=10, dim3=1) except NULL:
    print "getp()"

    cdef int *p = <int *> malloc(dim1 * dim2 * dim3 * sizeof(int))

    if p == NULL:
        raise MemoryError

    for i in range(dim1 * dim2 * dim3):
        p[i] = i

    return p

cdef void callback_free_data(void *p):
    print 'callback free data called'
    free(p)

def test_array_from_pointer():
    """
    >>> test_array_from_pointer()
    getp()
    69
    c
    getp()
    callback free data called
    fortran
    getp()
    56
    getp()
    56
    getp()
    119
    callback free data called
    """
    cdef int *p = getp()
    cdef array c_arr = <int[:10, :10]> p
    c_arr.callback_free_data = callback_free_data
    print c_arr[6, 9]
    print c_arr.mode

    c_arr = (<int[:10:1, :10]> getp())
    print c_arr.mode
    c_arr.callback_free_data = free

    c_arr =  <int[:10, :10]> getp()
    c_arr.callback_free_data = free
    cdef int[:, ::1] mslice = c_arr
    print mslice[5, 6]

    c_arr = <int[:12, :10]> getp(12, 10)
    c_arr.callback_free_data = free
    print c_arr[5, 6]

    cdef int m = 12
    cdef int n = 10
    c_arr = <int[:m, :n]> getp(m, n)
    c_arr.callback_free_data = callback_free_data
    print c_arr[m - 1, n - 1]

def test_array_from_pointer_3d():
    """
    >>> test_array_from_pointer_3d()
    getp()
    3 3
    True True
    """
    cdef int *p = getp(2, 2, 2)
    cdef array c_arr = <int[:2, :2, :2:1]> p
    cdef array f_arr = <int[:2:1, :2, :2]> p

    cdef int[:, :, ::1] m1 = c_arr
    cdef int[::1, :, :] m2 = f_arr

    print m1[0, 1, 1], m2[1, 1, 0]
    print m1.is_c_contig(), m2.is_f_contig()

def test_cyarray_from_carray():
    """
    >>> test_cyarray_from_carray()
    0 8 21
    0 8 21
    """
    cdef int[7][8] a
    for i in range(7):
        for j in range(8):
            a[i][j] = i * 8 + j

    cdef int[:, :] mslice = <int[:, :]> a
    print mslice[0, 0], mslice[1, 0], mslice[2, 5]

    mslice = a
    print mslice[0, 0], mslice[1, 0], mslice[2, 5]
