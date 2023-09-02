cdef int CHKERR(int ierr) except -1:
    if ierr==0: return 0
    raise RuntimeError

cdef int obj2int(object ob) except *:
    return ob

def foo(a):
    """
    >>> foo(0)
    >>> foo(1)
    Traceback (most recent call last):
    RuntimeError
    """
    cdef int i = obj2int(a)
    CHKERR(i)

cdef int* except_expr(bint fire) except <int*>-1:
    if fire:
        raise RuntimeError

def test_except_expr(bint fire):
    """
    >>> test_except_expr(False)
    >>> test_except_expr(True)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    except_expr(fire)

cdef double except_big_result(bint fire) except 100000000000000000000000000000000:
    if fire:
        raise RuntimeError

def test_except_big_result(bint fire):
    """
    >>> test_except_big_result(False)
    >>> test_except_big_result(True)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    except_big_result(fire)


cdef unsigned short except_promotion_compare(bint fire) except *:
    if fire:
        raise RuntimeError

def test_except_promotion_compare(bint fire):
    """
    >>> test_except_promotion_compare(False)
    >>> test_except_promotion_compare(True)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    except_promotion_compare(fire)


cdef int cdef_function_that_raises():
    raise RuntimeError

cdef int cdef_noexcept_function_that_raises() noexcept:
    raise RuntimeError

def test_except_raise_by_default():
    """
    >>> test_except_raise_by_default()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    cdef_function_that_raises()

def test_noexcept():
    """
    >>> test_noexcept()
    """
    cdef_noexcept_function_that_raises()


cdef int* cdef_ptr_func(int* input, int failure_mode):
    # should have except NULL? by default
    # failure mode is 0, 1, or 2
    if failure_mode == 0:
        return input  # don't fail
    elif failure_mode == 1:
        return NULL  # no exception
    else:
        raise RuntimeError("help!")

ctypedef int* (*cdef_ptr_func_ptr)(int*, int) except? NULL

def test_ptr_func(int failure_mode):
    """
    >>> test_ptr_func(0)
    100
    >>> test_ptr_func(1)
    NULL
    >>> test_ptr_func(2)
    exception
    """
    # check that the signature is what we think it is
    cdef cdef_ptr_func_ptr fptr = cdef_ptr_func
    cdef int a = 100
    try:
        out = fptr(&a, failure_mode)
        if out:
            return out[0]
        else:
            print("NULL")
    except RuntimeError:
        print("exception")

def test_ptr_func2(int failure_mode):
    """
    >>> test_ptr_func(0)
    100
    >>> test_ptr_func(1)
    NULL
    >>> test_ptr_func(2)
    exception
    """
    # as above, but don't go through a function pointer
    cdef int a = 100
    try:
        out = cdef_ptr_func(&a, failure_mode)
        if out:
            return out[0]
        else:
            print("NULL")
    except RuntimeError:
        print("exception")
