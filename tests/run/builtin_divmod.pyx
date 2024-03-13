# mode: run

def divmod_int_regular(a,b):
    """
    >>> divmod_int_regular(10,5)
    (2, 0)
    >>> divmod_int_regular(9191,4096)
    (2, 999)
    >>> divmod_int_regular(10000,10010)
    (0, 10000)
    >>> divmod_int_regular(-999999,-111111)
    (9, 0)
    >>> divmod_int_regular(-888888,-11111)
    (80, -8)
    >>> divmod_int_regular(-10000,-10086)
    (0, -10000)
    >>> divmod_int_regular(5,-1)
    (-5, 0)
    >>> divmod_int_regular(-40,3)
    (-14, 2)
    >>> divmod_int_regular(0,9)
    (0, 0)
    >>> divmod_int_regular(0,-987654321)
    (0, 0)
    """
    return divmod(a,b)


def divmod_by_0(a,b):
    """
    >>> divmod_by_0(33,0) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    return divmod(a,0)
