fn i32 CHKERR(i32 ierr) except -1:
    if ierr==0: return 0
    raise RuntimeError

fn i32 obj2int(object ob) except *:
    return ob

def foo(a):
    """
    >>> foo(0)
    >>> foo(1)
    Traceback (most recent call last):
    RuntimeError
    """
    let i32 i = obj2int(a)
    CHKERR(i)

fn i32* except_expr(bint fire) except <i32*>-1:
    if fire:
        raise RuntimeError

def test_except_expr(bint fire):
    """
    >>> test_except_expr(false)
    >>> test_except_expr(true)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    except_expr(fire)

fn f64 except_big_result(bint fire) except 100000000000000000000000000000000:
    if fire:
        raise RuntimeError

def test_except_big_result(bint fire):
    """
    >>> test_except_big_result(false)
    >>> test_except_big_result(true)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    except_big_result(fire)

fn u16 except_promotion_compare(bint fire) except *:
    if fire:
        raise RuntimeError

def test_except_promotion_compare(bint fire):
    """
    >>> test_except_promotion_compare(false)
    >>> test_except_promotion_compare(true)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    except_promotion_compare(fire)

fn i32 cdef_function_that_raises():
    raise RuntimeError

fn i32 cdef_noexcept_function_that_raises() noexcept:
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

fn i32* cdef_ptr_func(i32* input, i32 failure_mode):
    # should have except NULL? by default
    # failure mode is 0, 1, or 2
    if failure_mode == 0:
        return input  # don't fail
    elif failure_mode == 1:
        return NULL  # no exception
    else:
        raise RuntimeError("help!")

ctypedef i32* (*cdef_ptr_func_ptr)(i32*, i32) except? NULL

def test_ptr_func(i32 failure_mode):
    """
    >>> test_ptr_func(0)
    100
    >>> test_ptr_func(1)
    NULL
    >>> test_ptr_func(2)
    exception
    """
    # check that the signature is what we think it is
    let cdef_ptr_func_ptr fptr = cdef_ptr_func
    let i32 a = 100
    try:
        out = fptr(&a, failure_mode)
        if out:
            return out[0]
        else:
            print("NULL")
    except RuntimeError:
        print("exception")

def test_ptr_func2(i32 failure_mode):
    """
    >>> test_ptr_func(0)
    100
    >>> test_ptr_func(1)
    NULL
    >>> test_ptr_func(2)
    exception
    """
    # as above, but don't go through a function pointer
    let i32 a = 100
    try:
        out = cdef_ptr_func(&a, failure_mode)
        if out:
            return out[0]
        else:
            print("NULL")
    except RuntimeError:
        print("exception")
