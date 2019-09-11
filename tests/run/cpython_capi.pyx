# mode: run
# tag: c-api

from cpython cimport mem
from cpython.pystate cimport PyGILState_Ensure, PyGILState_Release, PyGILState_STATE


cdef short _assert_calloc(short* s, int n) except -1 with gil:
    """Assert array ``s`` of length ``n`` is zero and return 3."""
    s[0] += 1
    s[n - 1] += 3
    assert not s[0] and not s[n - 1]
    for i in range(1, n - 1):
        assert not s[i]
    return s[n - 1]


def test_pymalloc():
    """
    >>> test_pymalloc()
    3
    """
    cdef short i
    cdef short* s = <short*> mem.PyMem_Calloc(10, sizeof(short))
    if not s:
        raise MemoryError()
    try:
        i = _assert_calloc(s, 10)
    finally:
        mem.PyMem_Free(s)
    cdef char* m2
    cdef char* m = <char*> mem.PyMem_Malloc(20)
    assert m
    try:
        m[0] = 1
        m[1] = 2
        m[2] = i
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
    cdef short i
    cdef short* s
    cdef char* m
    cdef char* m2 = NULL
    with nogil:
        s = <short*> mem.PyMem_RawCalloc(10, sizeof(short))
        if not s:
            raise MemoryError()
        try:
            i = _assert_calloc(s, 10)
        finally:
            mem.PyMem_RawFree(s)
        m = <char*> mem.PyMem_RawMalloc(20)
        if not m:
            raise MemoryError()
        try:
            m[0] = 1
            m[1] = 2
            m[2] = i
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
