# mode: run
# tag: c-api

from __future__ import print_function

from cpython cimport mem, PyObject
from cpython.pystate cimport PyGILState_Ensure, PyGILState_Release, PyGILState_STATE
from cpython.dict cimport PyDict_GetItemRef, PyDict_GetItemStringRef, PyDict_SetDefaultRef 
from cpython.list cimport PyList_GetItemRef, PyList_Clear, PyList_Extend
from cpython.ref cimport Py_XDECREF

import sys

__doc__ = ""

def test_pymalloc():
    """
    >>> test_pymalloc()
    3
    """
    cdef char* m2
    cdef char* m = <char*> mem.PyMem_Malloc(20)
    assert m
    try:
        m[0] = 1
        m[1] = 2
        m[2] = 3
        m2 = <char*> mem.PyMem_Realloc(m, 10)
        assert m2
        m = m2
        return m[2]
    finally:
        mem.PyMem_Free(m)


def test_gilstate():
    """
    >>> test_gilstate()
    'ok'
    """

    # cython used to have invalid definition for PyGILState_STATE, which was
    # making the following code fail to compile
    cdef PyGILState_STATE gstate = PyGILState_Ensure()
    # TODO assert that GIL is taken
    PyGILState_Release(gstate)
    return 'ok'

def test_dict_getref(d):
    """
    >>> test_dict_getref({'key': ['value']})
    ['value']
    ['value']
    1 ['value']
    >>> test_dict_getref({})
    0 Ellipsis

    One further test is in the module __doc__ to exclude it for PyPy
    """
    cdef PyObject* o;
    if PyDict_GetItemRef(d, "key", &o):
        print(<object>o)
        Py_XDECREF(o)
    
    if PyDict_GetItemStringRef(d, "key", &o):
        print(<object>o)
        Py_XDECREF(o)
    
    was_in_dict = PyDict_SetDefaultRef(d, "key", Ellipsis, &o)
    print(was_in_dict, <object>o)
    Py_XDECREF(o)

if not hasattr(sys, 'pypy_version_info'):
    __doc__ += """
        >>> test_dict_getref("I'm not a dict")  #doctest: +ELLIPSIS
        Traceback (most recent call last):
        SystemError: ...
    """

def test_list_getref_extend_clear(list):
    """
    >>> test_list_getref_extend_clear([1, 2, 3])
    1
    [1, 2, 3, 4, 5]
    []
    >>> test_list_getref_extend_clear([])  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: ...
    """

    first = PyList_GetItemRef(list, 0)
    print(first)

    PyList_Extend(list, [4, 5])
    print(list)
    
    PyList_Clear(list)
    print(list)
