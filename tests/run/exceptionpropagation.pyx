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



cdef fused number_or_object:
    double
    int
    object

cdef number_or_object return_fused_type(number_or_object arg, bint fail):
    if fail:
        raise RuntimeError
    return arg

ctypedef double (*fused_ptr1)(double, bint) except? -1
ctypedef int (*fused_ptr2)(int, bint) except? -1
ctypedef object (*fused_ptr3)(object, bint)

def test_fused_number_or_object():
    """
    Make sure that fused functions default to the appropriate exception type

    >>> test_fused_number_or_object()
    """
    # Test that we can assign to the function pointer we expect
    cdef fused_ptr1 p1 = return_fused_type[double]
    cdef fused_ptr2 p2 = return_fused_type[int]
    cdef fused_ptr3 p3 = return_fused_type[object]

    # call double variants
    print(return_fused_type(1.0, False))
    print(return_fused_type(-1.0, False))
    try:
        print(return_fused_type(2.0, True))
        assert False, "Should not reach here"
    except RuntimeError:
        pass

    # Call int variants
    print(return_fused_type(1, False))
    print(return_fused_type(-1, False))
    try:
        print(return_fused_type(2, True))
        assert False, "Should not reach here"
    except RuntimeError:
        pass

    # Call object variants
    print(return_fused_type(None, False))
    try:
        print(return_fused_type(None, True))
        assert False, "Should not reach here"
    except RuntimeError:
        pass

cdef fused number:
    double
    int

# TODO: this doesn't work
# test that we can manually set the return value
#cdef number return_fused_type_manual(number arg, bint fail) except -2:
#    if fail:
#        raise RuntimeError
#    return arg
#
#ctypedef double (*fused_manual_ptr1)(double, bint) except? -2
#ctypedef int (*fused_manual_ptr2)(int, bint) except -2
#
#def test_fused_number_or_object_manual():
#    """
#    >>> test_fused_number_or_object_manual()
#    """
#    # test that the pointer assignment works like we think it should
#    cdef fused_manual_ptr1 p1 = return_fused_type_manual[double]
#    cdef fused_manual_ptr1 p2 = return_fused_type_manual[int]
#
#    # double
#    print(test_fused_number_or_object_manual(-1.0, False))
#    try:
#        print(test_fused_number_or_object_manual(-1.0, True))
#        assert False, "Should not reach here"
#    except RuntimeError:
#        pass
#
#    # int
#    print(test_fused_number_or_object_manual(-1, False))
#    try:
#        print(test_fused_number_or_object_manual(-1.0, True))
#        assert False, "Should not reach here"
#    except RuntimeError:
#        pass

cdef number return_fused_type_noexcept(number x) noexcept:
    return x

ctypedef double (*fused_noexcept_ptr1)(double, bint) noexcept
ctypedef int (*fused_noexcept_ptr2)(int, bint) noexcept

def test_fused_noexcept():
    """
    >>> test_fused_noexcept()
    """
    # check the pointer types match
    cdef fused_noexcept_ptr1 p1 = return_fused_type_noexcept[double]
    cdef fused_noexcept_ptr2 p2 = return_fused_type_noexcept[int]

    # double
    print(return_fused_type_noexcept(1.0))

    # int
    print(return_fused_type_noexcept(1))
