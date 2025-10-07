# mode: run

cdef bint is_null(int* x):
    return False # disabled - currently just a parser test
    match x:
        case NULL:
            return True
        case _:
            return False

def test_is_null():
    """
    >>> test_is_null()
    """
    cdef int some_int = 1
    return  # disabled - currently just a parser test
    assert is_null(&some_int) == False
    assert is_null(NULL) == True
