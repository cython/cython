# mode: run

# Tests the builtin memoryview - there's an '_' in the file name
# just so it isn't tied to Cython memoryview lests

from __future__ import print_function

cimport cython
#from cpython.memoryview cimport PyMemoryView_GET_BUFFER

@cython.test_fail_if_path_exists("//SimpleCallNode")
def test_convert_from_obj(o):
    """
    >>> abc = b'abc'
    >>> test_convert_from_obj(abc).obj == abc
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
    >>> mview.obj == b'argh!'
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
