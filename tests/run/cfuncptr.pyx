# mode: run


cdef int grail():
    cdef int (*spam)()
    spam = &grail
    spam = grail
    assert spam is grail
    assert spam == grail
    assert spam == &grail


ctypedef int funcptr_t()

cdef funcptr_t* get_grail():
    return &grail


def test_assignments():
    """
    >>> test_assignments()
    """
    grail()


def test_return_value():
    """
    >>> test_return_value()
    True
    """
    g = get_grail()
    return g == &grail


def call_cfuncptr():
    """
    >>> call_cfuncptr()
    """
    cdef int (*spam)()
    spam = grail
    spam()

cdef int exceptminus2(int bad) except -2:
    if bad:
        raise RuntimeError
    else:
        return 0

def call_exceptminus2(bad):
    """
    >>> call_exceptminus2(True)
    Traceback (most recent call last):
    ...
    RuntimeError
    >>> call_exceptminus2(False)
    0
    """
    cdef int (*fptr)(int) except *  # GH4770 - should not be treated as except? -1
    fptr = exceptminus2
    return fptr(bad)
