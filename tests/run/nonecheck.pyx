__doc__ = u"""
Tests accessing attributes of extension type variables
set to None
"""

cimport cython

cdef class MyClass:
    cdef int a, b
    def __init__(self, a, b):
        self.a = a
        self.b = b

@cython.nonecheck(True)
def getattr_(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> getattr_(obj)
    2
    >>> getattr_(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    >>> setattr_(obj)
    >>> getattr_(obj)
    10
    """
    print var.a

@cython.nonecheck(True)
def setattr_(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> setattr_(obj)
    >>> setattr_(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    """
    var.a = 10

@cython.nonecheck(True)
def getattr_nogil(MyClass var):
    """
    >>> getattr_nogil(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    """
    with nogil:
        var.a

@cython.nonecheck(True)
def setattr_nogil(MyClass var):
    """
    >>> setattr_nogil(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    """
    with nogil:
        var.a = 1

def some():
    return MyClass(4, 5)

@cython.nonecheck(True)
def checking(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> checking(obj)
    2
    2
    >>> checking(None)
    var is None
    """
    state = (var is None)
    if not state:
        print var.a
    if var is not None:
        print var.a
    else:
        print u"var is None"

@cython.nonecheck(True)
def check_and_assign(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> check_and_assign(obj)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    """
    if var is not None:
        print var.a
        var = None
        print var.a

@cython.nonecheck(True)
def check_buffer_get(object[int] buf):
    """
    >>> check_buffer_get(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    return buf[0]

@cython.nonecheck(True)
def check_buffer_set(object[int] buf):
    """
    >>> check_buffer_set(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    buf[0] = 1

@cython.nonecheck(True)
def test_memslice_get(double[:] buf):
    """
    >>> test_memslice_get(None)
    Traceback (most recent call last):
    TypeError: Cannot index None memoryview slice
    """
    return buf[0]

@cython.nonecheck(True)
def test_memslice_set(double[:] buf):
    """
    >>> test_memslice_set(None)
    Traceback (most recent call last):
    TypeError: Cannot index None memoryview slice
    """
    buf[0] = 1.0

@cython.nonecheck(True)
def test_memslice_copy(double[:] buf):
    """
    >>> test_memslice_copy(None)
    Traceback (most recent call last):
    AttributeError: Cannot access 'copy' attribute of None memoryview slice
    """
    cdef double[:] copy = buf.copy()

@cython.nonecheck(True)
def test_memslice_transpose(double[:] buf):
    """
    >>> test_memslice_transpose(None)
    Traceback (most recent call last):
    AttributeError: Cannot transpose None memoryview slice
    """
    cdef double[:] T = buf.T

@cython.nonecheck(True)
def test_memslice_shape(double[:] buf):
    """
    >>> test_memslice_shape(None)
    Traceback (most recent call last):
    AttributeError: Cannot access 'shape' attribute of None memoryview slice
    """
    cdef Py_ssize_t extent = buf.shape[0]

@cython.nonecheck(True)
def test_memslice_slice(double[:] buf):
    """
    >>> test_memslice_slice(None)
    Traceback (most recent call last):
    TypeError: Cannot slice None memoryview slice
    """
    cdef double[:] sliced = buf[1:]

@cython.nonecheck(True)
def test_memslice_slice2(double[:] buf):
    """
    Should this raise an error? It may not slice at all.
    >>> test_memslice_slice(None)
    Traceback (most recent call last):
    TypeError: Cannot slice None memoryview slice
    """
    cdef double[:] sliced = buf[:]

@cython.nonecheck(True)
def test_memslice_slice_assign(double[:] buf):
    """
    >>> test_memslice_slice_assign(None)
    Traceback (most recent call last):
    TypeError: Cannot assign to None memoryview slice
    """
    buf[...] = 2

@cython.nonecheck(True)
def test_memslice_slice_assign2(double[:] buf):
    """
    >>> test_memslice_slice_assign2(None)
    Traceback (most recent call last):
    TypeError: Cannot slice None memoryview slice
    """
    buf[:] = buf[::-1]
