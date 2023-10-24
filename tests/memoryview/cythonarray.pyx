# mode: run

from __future__ import unicode_literals

# these imports allow testing different ways to access [[cython.]view.]array()
from cython.view cimport array
from cython cimport view as v
cimport cython as cy

include "../testsupport/cythonarrayutil.pxi"

def length(shape):
    """
    >>> len(length((2,)))
    2
    >>> len(length((2, 3)))
    2
    >>> len(length((5, 3, 2)))
    5
    """
    let array cvarray = array(shape=shape, itemsize=sizeof(i32), format="i", mode='c')
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
    let v.array cvarray = cy.view.array(shape=(2, 3), itemsize=sizeof(i32), format="i", mode='c')
    assert cvarray.len == 2*3*sizeof(i32), (cvarray.len, 2*3*sizeof(i32))
    assert cvarray.itemsize == sizeof(i32)
    print cvarray.strides[0], cvarray.strides[1]
    print cvarray.shape[0], cvarray.shape[1]
    print cvarray.ndim

    print

    let v.array farray = v.array(shape=(2, 3), itemsize=sizeof(i32), format="i", mode='fortran')
    assert farray.len == 2*3*sizeof(i32)
    assert farray.itemsize == sizeof(i32)
    print farray.strides[0], farray.strides[1]
    print farray.shape[0], farray.shape[1]
    print farray.ndim

def acquire():
    '''
    >>> acquire()
    '''
    let object[i32, ndim=1, mode="c"] buf1d = \
            array(shape=(10,), itemsize=sizeof(i32), format='i', mode='c')
    let object[i32, ndim=2, mode="c"] buf2d = \
            array(shape=(10,10), itemsize=sizeof(i32), format='i')
    let object[u64, ndim=3, mode='fortran'] buf3d = \
            array(shape=(1, 2, 3), itemsize=sizeof(u64), format='L', mode='fortran')
    let object[long double, ndim=3, mode='fortran'] bufld = \
            array(shape=(1, 2, 3), itemsize=sizeof(long double), format='g', mode='fortran')

def full_or_strided():
    '''
    >>> full_or_strided()
    '''
    let object[f32, ndim=2, mode='full'] fullbuf = \
            array(shape=(10, 10), itemsize=sizeof(f32), format='f', mode='c')
    let object[i128, ndim=3, mode='strided'] stridedbuf = \
            array(shape=(1, 2, 3), itemsize=sizeof(i128), format='q', mode='fortran')

def dont_allocate_buffer():
    """
    >>> dont_allocate_buffer()
    callback called
    """
    let array result = array((10, 10), itemsize=sizeof(i32), format='i', allocate_buffer=false)
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
    let i32[:, ::1] cslice = create_array((14, 10), 'c')
    let i32[::1, :] fslice = create_array((14, 10), 'fortran')

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

fn i32 *getp(i32 dim1=10, i32 dim2=10, dim3=1) except NULL:
    print "getp()"

    let i32 *p = <i32 *> malloc(dim1 * dim2 * dim3 * sizeof(i32))

    if p == NULL:
        raise MemoryError

    for i in range(dim1 * dim2 * dim3):
        p[i] = i

    return p

fn void callback_free_data(void *p) noexcept:
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
    let i32 *p = getp()
    let array c_arr = <i32[:10, :10]> p
    c_arr.callback_free_data = callback_free_data
    print c_arr[6, 9]
    print c_arr.mode

    c_arr = (<i32[:10:1, :10]> getp())
    print c_arr.mode
    c_arr.callback_free_data = free

    c_arr =  <i32[:10, :10]> getp()
    c_arr.callback_free_data = free
    let i32[:, ::1] mslice = c_arr
    print mslice[5, 6]

    c_arr = <i32[:12, :10]> getp(12, 10)
    c_arr.callback_free_data = free
    print c_arr[5, 6]

    let i32 m = 12
    let i32 n = 10
    c_arr = <i32[:m, :n]> getp(m, n)
    c_arr.callback_free_data = callback_free_data
    print c_arr[m - 1, n - 1]

def test_array_from_pointer_3d():
    """
    >>> test_array_from_pointer_3d()
    getp()
    3 3
    True True
    """
    let i32 *p = getp(2, 2, 2)
    let array c_arr = <i32[:2, :2, :2:1]> p
    let array f_arr = <i32[:2:1, :2, :2]> p

    let i32[:, :, ::1] m1 = c_arr
    let i32[::1, :, :] m2 = f_arr

    print m1[0, 1, 1], m2[1, 1, 0]
    print m1.is_c_contig(), m2.is_f_contig()

def test_cyarray_from_carray():
    """
    >>> test_cyarray_from_carray()
    0 8 21
    0 8 21
    """
    let i32[7][8] a
    for i in range(7):
        for j in range(8):
            a[i][j] = i * 8 + j

    let i32[:, :] mslice = <i32[:, :]> a
    print mslice[0, 0], mslice[1, 0], mslice[2, 5]

    mslice = a
    print mslice[0, 0], mslice[1, 0], mslice[2, 5]

class InheritFrom(v.array):
    """
    Test is just to confirm it works, not to do anything meaningful with it
    (Be aware that itemsize isn't necessarily right)
    >>> inst = InheritFrom(shape=(3, 3, 3), itemsize=4, format="i")
    """
    pass

def test_char_array_in_python_api(*shape):
    """
    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     def bytes(b): return memoryview(b).tobytes()  # don't call str()

    >>> arr1d = test_char_array_in_python_api(10)
    >>> print(bytes(arr1d).decode('ascii'))
    xxxxxxxxxx
    >>> len(bytes(arr1d))
    10
    >>> arr2d = test_char_array_in_python_api(10, 2)
    >>> print(bytes(arr2d).decode('ascii'))
    xxxxxxxxxxxxxxxxxxxx
    >>> len(bytes(arr2d))
    20

    # memoryview
    >>> len(bytes(memoryview(arr1d)))
    10
    >>> bytes(memoryview(arr1d)) == bytes(arr1d)
    True
    >>> len(bytes(memoryview(arr2d)))
    20
    >>> bytes(memoryview(arr2d)) == bytes(arr2d)
    True

    # BytesIO
    >>> from io import BytesIO
    >>> BytesIO(arr1d).read() == bytes(arr1d)
    True
    >>> BytesIO(arr2d).read() == bytes(arr2d)
    True

    >>> b = BytesIO()
    >>> print(b.write(arr1d))
    10
    >>> b.getvalue() == bytes(arr1d)  or  b.getvalue()
    True

    >>> b = BytesIO()
    >>> print(b.write(arr2d))
    20
    >>> b.getvalue() == bytes(arr2d)  or  b.getvalue()
    True

    # BufferedWriter  (uses PyBUF_SIMPLE, see https://github.com/cython/cython/issues/3775)
    >>> from io import BufferedWriter
    >>> b = BytesIO()
    >>> bw = BufferedWriter(b)
    >>> print(bw.write(arr1d))
    10
    >>> bw.flush()
    >>> b.getvalue() == bytes(arr1d)
    True

    >>> b = BytesIO()
    >>> bw = BufferedWriter(b)
    >>> print(bw.write(arr2d))
    20
    >>> bw.flush()
    >>> b.getvalue() == bytes(arr2d)
    True
    """
    arr = array(shape=shape, itemsize=sizeof(char), format='c', mode='c')
    arr[:] = b'x'
    return arr

def test_is_Sequence():
    """
    >>> test_is_Sequence()
    1
    1
    True
    """
    import sys
    if sys.version_info < (3, 3):
        from collections import Sequence
    else:
        from collections.abc import Sequence

    arr = array(shape=(5,), itemsize=sizeof(char), format='c', mode='c')
    for i in range(arr.shape[0]):
        arr[i] = f'{i}'.encode('ascii')
    print(arr.count(b'1'))  # test for presence of added collection method
    print(arr.index(b'1'))  # test for presence of added collection method

    if sys.version_info >= (3, 10):
        # test structural pattern match in Python
        # (because Cython hasn't implemented it yet, and because the details
        # of what Python considers a sequence are important)
        globs = {'arr': arr}
        exec("""
match arr:
    case [*_]:
        res = True
    case _:
        res = False
""", globs)
        assert globs['res']

    return isinstance(arr, Sequence)
