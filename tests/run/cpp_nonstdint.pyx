# tag: cpp

cdef extern from "cpp_nonstdint.h":
    ctypedef int Int24
    ctypedef int Int56
    ctypedef int Int88
    ctypedef int Int512

cdef object one = 1

# ---

INT24_MAX = (one<<(sizeof(Int24)*8-1))-one
INT24_MIN = (-INT24_MAX-one)

def test_int24(Int24 i):
    """
    >>> str(test_int24(-1))
    '-1'
    >>> str(test_int24(0))
    '0'
    >>> str(test_int24(1))
    '1'

    >>> test_int24(INT24_MAX) == INT24_MAX
    True
    >>> test_int24(INT24_MIN) == INT24_MIN
    True

    >>> test_int24(INT24_MIN-1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...
    >>> test_int24(INT24_MAX+1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    >>> test_int24("123") #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    return i

# ---

INT56_MAX = (one<<(sizeof(Int56)*8-1))-one
INT56_MIN = (-INT56_MAX-one)

def test_int56(Int56 i):
    """
    >>> str(test_int56(-1))
    '-1'
    >>> str(test_int56(0))
    '0'
    >>> str(test_int56(1))
    '1'

    >>> test_int56(INT56_MAX) == INT56_MAX
    True
    >>> test_int56(INT56_MIN) == INT56_MIN
    True

    >>> test_int56(INT56_MIN-1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...
    >>> test_int56(INT56_MAX+1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    >>> test_int56("123") #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    return i

# ---

INT88_MAX = (one<<(sizeof(Int88)*8-1))-one
INT88_MIN = (-INT88_MAX-one)

def test_int88(Int88 i):
    """
    >>> str(test_int88(-1))
    '-1'
    >>> str(test_int88(0))
    '0'
    >>> str(test_int88(1))
    '1'

    >>> test_int88(INT88_MAX) == INT88_MAX
    True
    >>> test_int88(INT88_MIN) == INT88_MIN
    True

    >>> test_int88(INT88_MIN-1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...
    >>> test_int88(INT88_MAX+1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    >>> test_int88("123") #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    return i

# ---

INT512_MAX = (one<<(sizeof(Int512)*8-1))-one
INT512_MIN = (-INT512_MAX-one)

def test_int512(Int512 i):
    """
    >>> str(test_int512(-1))
    '-1'
    >>> str(test_int512(0))
    '0'
    >>> str(test_int512(1))
    '1'

    >>> test_int512(INT512_MAX) == INT512_MAX
    True
    >>> test_int512(INT512_MIN) == INT512_MIN
    True

    >>> test_int512(INT512_MIN-1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...
    >>> test_int512(INT512_MAX+1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    >>> test_int512("123") #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    return i

# ---
