# mode: run

import cython

def divmod_regular(a,b):
    """
    >>> divmod_regular(10,5)
    (2, 0)
    >>> divmod_regular(9191,4096)
    (2, 999)
    >>> divmod_regular(10000,10010)
    (0, 10000)
    >>> divmod_regular(-999999,-111111)
    (9, 0)
    >>> divmod_regular(-888888,-11111)
    (80, -8)
    >>> divmod_regular(-10000,-10086)
    (0, -10000)
    >>> divmod_regular(5,-1)
    (-5, 0)
    >>> divmod_regular(-40,3)
    (-14, 2)
    >>> divmod_regular(11,-3)
    (-4, -1)
    >>> divmod_regular(0,9)
    (0, 0)
    >>> divmod_regular(0,-987654321)
    (0, 0)

    >>> divmod_regular(33,0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    return divmod(a,b)


@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'divmod']",
                                "//ReturnStatNode//NameNode[@entry.cname = '__Pyx_divmod_int']")
def divmod_int_regular(a: cython.int, b: cython.int):
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
    >>> divmod_int_regular(-50,1)
    (-50, 0)
    >>> divmod_int_regular(-40,3)
    (-14, 2)
    >>> divmod_int_regular(11,-3)
    (-4, -1)
    >>> divmod_int_regular(0,9)
    (0, 0)
    >>> divmod_int_regular(0,-987654321)
    (0, 0)

    >>> divmod_int_regular(33,0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    return divmod(a,b)
