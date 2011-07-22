# mode: run

from __future__ import unicode_literals

# from cython cimport array
# cimport cython.array as array
cimport cython as cy
# array = cython.array

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
    callback called 1
    """
    cdef cy.array result = cy.array((10, 10), itemsize=sizeof(int), format='i', allocate_buffer=False)
    assert result.data == NULL
    result.data = <char *> 1
    result.callback_free_data = callback
    result = None

cdef void callback(char *data):
    print "callback called %d" % <long> data
