# mode: run
# tag: c-api

# PyMem_RawMalloc tests that need to be disabled for Python < 3.5
# (some of these would work of Python 3.4, but it's easier to disable
# them in one place)

from cpython cimport mem

cdef short _assert_calloc(short* s, int n) except -1 with gil:
    """Assert array ``s`` of length ``n`` is zero and return 3."""
    assert not s[0] and not s[n - 1]
    s[0] += 1
    s[n - 1] += 3
    for i in range(1, n - 1):
        assert not s[i]
    return s[n - 1]

def test_pycalloc():
    """
    >>> test_pycalloc()
    3
    """
    cdef short* s = <short*> mem.PyMem_Calloc(10, sizeof(short))
    if not s:
        raise MemoryError()
    try:
        return _assert_calloc(s, 10)
    finally:
        mem.PyMem_Free(s)

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
