# mode: run

from __future__ import print_function

cimport cython
#from cpython.memoryview cimport PyMemoryView_GET_BUFFER

@cython.test_fail_if_path_exists("//SimpleCallNode")
def test_convert_from_obj(o):
    """
    >>> abc = b'abc'
    >>> all(x == y for x, y in zip(test_convert_from_obj(abc), abc))
    True
    """
    return memoryview(o)

# TODO - this currently doesn't work because the buffer fails a
# "can coerce to python object" test earlier. But it'd be nice to support
'''
def test_create_from_buffer():
    """
    memoryview from Py_buffer exists and is special-cased
    >>> mview = test_create_from_buffer()
    >>> >>> all(x == y for x, y in zip(mview, b'argh!'))
    True
    """
    other_view = memoryview(b'argh!')
    cdef Py_buffer *buf = PyMemoryView_GET_BUFFER(other_view)
    return memoryview(buf)
'''

@cython.test_fail_if_path_exists("//AttributeNode")
def test_optimized_attributes(memoryview view):
    """
    >>> test_optimized_attributes(memoryview(b'zzzzz'))
    1 1 True
    """
    print(view.itemsize, view.ndim, view.readonly)
