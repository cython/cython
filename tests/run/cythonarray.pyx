# mode: run

from __future__ import unicode_literals

from cython cimport array
cimport cython as cy

include "cythonarrayutil.pxi"


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
    cdef cy.array cvarray = cy.array(shape=(2,3), itemsize=sizeof(int), format="i", mode='c')
    assert cvarray.len == 2*3*sizeof(int), (cvarray.len, 2*3*sizeof(int))
    assert cvarray.itemsize == sizeof(int)
    print cvarray.strides[0], cvarray.strides[1]
    print cvarray.shape[0], cvarray.shape[1]
    print cvarray.ndim

    print

    cdef cy.array farray = cy.array(shape=(2,3), itemsize=sizeof(int), format="i", mode='fortran')
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
            cy.array(shape=(10,), itemsize=sizeof(int), format='i', mode='c')
    cdef object[int, ndim=2, mode="c"] buf2d = \
            cy.array(shape=(10,10), itemsize=sizeof(int), format='i')
    cdef object[unsigned long, ndim=3, mode='fortran'] buf3d = \
            cy.array(shape=(1,2,3), itemsize=sizeof(unsigned long), format='L', mode='fortran')
    cdef object[long double, ndim=3, mode='fortran'] bufld = \
            cy.array(shape=(1,2,3), itemsize=sizeof(long double), format='g', mode='fortran')

def full_or_strided():
    '''
    >>> full_or_strided()
    '''
    cdef object[float, ndim=2, mode='full'] fullbuf = \
            cy.array(shape=(10,10), itemsize=sizeof(float), format='f', mode='c')
    cdef object[long long int, ndim=3, mode='strided'] stridedbuf = \
            cy.array(shape=(1,2,3), itemsize=sizeof(long long int), format='q', mode='fortran')

def dont_allocate_buffer():
    """
    >>> dont_allocate_buffer()
    callback called
    """
    cdef cy.array result = cy.array((10, 10), itemsize=sizeof(int), format='i', allocate_buffer=False)
    assert result.data == NULL
    result.data = <char *> 1
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

cdef int *getp(int dim1=10, int dim2=10) except NULL:
    print "getp()"

    cdef int *p = <int *> malloc(dim1 * dim2 * sizeof(int))

    if p == NULL:
        raise MemoryError

    for i in range(dim1 * dim2):
        p[i] = i

    return p

cdef void callback_free_data(char *p):
    print 'callback free data called'
    free(p)

def test_array_from_pointer():
    """
    >>> test_array_from_pointer()
    getp()
    69
    c
    getp()
    fortran
    getp()
    56
    getp()
    56
    callback free data called
    """
    cdef int *p = getp()
    cdef array c_arr = <int[:10, :10]> p
    c_arr.callback_free_data = callback_free_data
    print c_arr[6, 9]
    print c_arr.mode

    print (<int[:10:1, :10]> getp()).mode

    cdef int[:, ::1] mslice = <int[:10, :10]> getp()
    print mslice[5, 6]
    print (<int[:12, :10]> getp(12, 10))[5, 6]

    # There is a reference cycle between the array object to its memoryview
    # object that it keeps
    del c_arr
    import gc
    gc.collect()
