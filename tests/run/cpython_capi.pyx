# mode: run
# tag: c-api

from __future__ import print_function

from cpython cimport mem, PyObject
from cpython.pystate cimport PyGILState_Ensure, PyGILState_Release, PyGILState_STATE
from cpython.dict cimport PyDict_GetItemRef, PyDict_GetItemStringRef, PyDict_SetDefaultRef 
from cpython.ref cimport Py_XDECREF


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
    >>> test_dict_getref("I'm not a dict")  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    SystemError: ...
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
