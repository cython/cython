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
