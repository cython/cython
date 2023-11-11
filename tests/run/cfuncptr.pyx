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

def call_exceptminus2_through_exceptstar_pointer(bad):
    """
    >>> call_exceptminus2_through_exceptstar_pointer(True)
    Traceback (most recent call last):
    ...
    RuntimeError
    >>> call_exceptminus2_through_exceptstar_pointer(False)
    0
    """
    cdef int (*fptr)(int) except *  # GH4770 - should not be treated as except? -1
    fptr = exceptminus2
    return fptr(bad)

def call_exceptminus2_through_exceptmaybeminus2_pointer(bad):
    """
    >>> call_exceptminus2_through_exceptmaybeminus2_pointer(True)
    Traceback (most recent call last):
    ...
    RuntimeError
    >>> call_exceptminus2_through_exceptmaybeminus2_pointer(False)
    0
    """
    cdef int (*fptr)(int) except ?-2  # exceptions should be compatible
    fptr = exceptminus2
    return fptr(bad)

cdef int noexcept_func():  # noexcept
    return 0

def call_noexcept_func_except_star():
    """
    >>> call_noexcept_func_except_star()
    0
    """
    cdef int (*fptr)() except *
    fptr = noexcept_func  # exception specifications are compatible
    return fptr()

def call_noexcept_func_except_check():
    """
    >>> call_noexcept_func_except_check()
    0
    """
    cdef int (*fptr)() except ?-1
    fptr = noexcept_func  # exception specifications are compatible
    return fptr()
