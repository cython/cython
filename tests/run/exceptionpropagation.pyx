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

cdef int cdef_function_that_raises_noexcept() noexcept:
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
    cdef_function_that_raises_noexcept()


cdef int return_value
