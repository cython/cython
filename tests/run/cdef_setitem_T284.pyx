# ticket: 284

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

def with_external_list(list L):
    """
    >>> with_external_list([1,2,3])
    [1, -10, 3]
    >>> with_external_list(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    ob = 1L
    L[ob] = -10
    return L

def test_list(list L, object i, object a):
    """
    >>> test_list(list(range(11)), -2, None)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, None, 10]
    >>> test_list(list(range(11)), "invalid index", None) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: list ... must be ...integer...
    """
    L[i] = a
    return L
