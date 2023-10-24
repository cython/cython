# mode: run


fn i32 grail():
    let i32 (*spam)()
    spam = &grail
    spam = grail
    assert spam is grail
    assert spam == grail
    assert spam == &grail

ctypedef i32 funcptr_t()

fn funcptr_t* get_grail():
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
    let i32 (*spam)()
    spam = grail
    spam()

fn i32 exceptminus2(i32 bad) except -2:
    if bad:
        raise RuntimeError
    else:
        return 0

def call_exceptminus2_through_exceptstar_pointer(bad):
    """
    >>> call_exceptminus2_through_exceptstar_pointer(true)
    Traceback (most recent call last):
    ...
    RuntimeError
    >>> call_exceptminus2_through_exceptstar_pointer(false)
    0
    """
    let i32 (*fptr)(i32) except *  # GH4770 - should not be treated as except? -1
    fptr = exceptminus2
    return fptr(bad)

def call_exceptminus2_through_exceptmaybeminus2_pointer(bad):
    """
    >>> call_exceptminus2_through_exceptmaybeminus2_pointer(true)
    Traceback (most recent call last):
    ...
    RuntimeError
    >>> call_exceptminus2_through_exceptmaybeminus2_pointer(false)
    0
    """
    let i32 (*fptr)(i32) except ?-2  # exceptions should be compatible
    fptr = exceptminus2
    return fptr(bad)

fn i32 noexcept_func():  # noexcept
    return 0

def call_noexcept_func_except_star():
    """
    >>> call_noexcept_func_except_star()
    0
    """
    let i32 (*fptr)() except *
    fptr = noexcept_func  # exception specifications are compatible
    return fptr()

def call_noexcept_func_except_check():
    """
    >>> call_noexcept_func_except_check()
    0
    """
    let i32 (*fptr)() except ?-1
    fptr = noexcept_func  # exception specifications are compatible
    return fptr()
