# mode: run
# tag: c-api

from cpython cimport mem
from cpython.pystate cimport PyGILState_Ensure, PyGILState_Release, PyGILState_STATE


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


def test_pymalloc_raw():
    """
    >>> test_pymalloc_raw()
    3
    """
    cdef char* m
    cdef char* m2 = NULL
    with nogil:
        m = <char*> mem.PyMem_RawMalloc(20)
        if not m:
            raise MemoryError()
        try:
            m[0] = 1
            m[1] = 2
            m[2] = 3
            m2 = <char*> mem.PyMem_RawRealloc(m, 10)
            if m2:
                m = m2
            retval = m[2]
        finally:
            mem.PyMem_RawFree(m)
    assert m2
    return retval


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
