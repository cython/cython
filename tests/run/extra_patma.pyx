# mode: run

cdef bint is_null(int* x):
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


# Pattern matching adopts a slightly stricter approach
# that most of Cython to what "is" an exact bool. Specifically
# regular C ints will never match, while c bints and Python
# objects can match
def match_pybool(x):
    """
    >>> match_pybool(False)
    is False
    >>> match_pybool(True)
    is True
    >>> match_pybool(None)
    is neither
    >>> match_pybool(1)
    is neither
    >>> match_pybool(0)
    is neither
    """
    match x:
        case False:
            print("is False")
        case True:
            print("is True")
        case _:
            print("is neither")

def match_c_bint(bint x):
    """
    >>> match_c_bint(False)
    is False
    >>> match_c_bint(True)
    is True
    """
    match x:
        case False:
            print("is False")
        case True:
            print("is True")
        case _:
            print("is neither")

def match_c_int(int x):
    """
    >>> match_c_int(0)
    is neither
    >>> match_c_int(1)
    is neither
    >>> match_c_int(100)
    is neither
    >>> match_c_int(-1)
    is neither
    """
    match x:
        case False:
            print("is False")
        case True:
            print("is True")
        case _:
            print("is neither")

