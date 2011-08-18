# mode: run
# tag: werror
# ticket: 714

def test_ptr():
    """
    >>> test_ptr()
    123
    """
    cdef int a
    cdef int *ptr

    ptr = &a
    ptr[0] = 123
    return a
