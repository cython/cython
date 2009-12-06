def no_cdef():
    """
    >>> no_cdef()
    """
    cdef object lst = list(range(11))
    ob = 10L
    lst[ob] = -10
    cdef object dd = {}
    dd[ob] = -10

def with_cdef():
    """
    >>> with_cdef()
    """
    cdef list lst = list(range(11))
    ob = 10L
    lst[ob] = -10
    cdef dict dd = {}
    dd[ob] = -10

def test_list(list L, object i, object a):
    """
    >>> test_list(list(range(11)), -2, None)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, None, 10]
    >>> test_list(list(range(11)), "invalid index", None) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: list indices must be integers...
    """
    L[i] = a
    return L
