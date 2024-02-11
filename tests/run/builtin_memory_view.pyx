# mode: run

# Tests Python's builtin memoryview.

from __future__ import print_function

import sys

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

def test_isinstance(x):
    """
    >>> test_isinstance(b"abc")
    False
    >>> test_isinstance(memoryview(b"abc"))
    True
    """
    return isinstance(x, memoryview)

def test_in_with(x):
    """
    This is really just a compile test. An optimization was being
    applied in a way that generated invalid code
    >>> test_in_with(b"abc")
    98
    """
    with memoryview(x) as xv:
        print(xv[1])


def test_returned_type():
    """
    This is really just a compile test. An optimization was being
    applied in a way that generated invalid code
    >>> test_returned_type()
    98
    """
    def foo() -> memoryview:
        rv = memoryview(b"abc")[:]
        return rv

    print(foo()[1])
