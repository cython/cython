# mode: run

import cython

def divmod_regular(a,b):
    """
    >>> divmod_regular(10, 5)
    (2, 0)
    >>> divmod_regular(4399, 2048)
    (2, 303)
    >>> divmod_regular(88321773, 98539211)
    (0, 88321773)
    >>> divmod_regular(-999999, -111111)
    (9, 0)
    >>> divmod_regular(-888888, -11111)
    (80, -8)
    >>> divmod_regular(-88837244, -110119120)
    (0, -88837244)
    >>> divmod_regular(5000000, -1)
    (-5000000, 0)
    >>> divmod_regular(-40, 3)
    (-14, 2)
    >>> divmod_regular(11, -3)
    (-4, -1)
    >>> divmod_regular(0, 996007985)
    (0, 0)
    >>> divmod_regular(0, -987654321)
    (0, 0)

    >>> divmod_regular(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    return divmod(a,b)


@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'divmod']",
                                "//ReturnStatNode//NameNode[@entry.cname = '__Pyx_divmod_int']")
def divmod_int_regular(a: cython.int, b: cython.int):
    """
    >>> divmod_int_regular(10, 5)
    (2, 0)
    >>> divmod_int_regular(9191, 4096)
    (2, 999)
    >>> divmod_int_regular(10000, 10010)
    (0, 10000)
    >>> divmod_int_regular(-999999, -111111)
    (9, 0)
    >>> divmod_int_regular(-888888, -11111)
    (80, -8)
    >>> divmod_int_regular(-10000, -10086)
    (0, -10000)
    >>> divmod_int_regular(-50, 1)
    (-50, 0)
    >>> divmod_int_regular(-40, 3)
    (-14, 2)
    >>> divmod_int_regular(11, -3)
    (-4, -1)
    >>> divmod_int_regular(0, 9)
    (0, 0)
    >>> divmod_int_regular(0, -987654321)
    (0, 0)

    >>> divmod_int_regular(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    return divmod(a,b)


@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'divmod']",
                                "//ReturnStatNode//NameNode[@entry.cname = '__Pyx_divmod_long']")
def divmod_long_regular(a: cython.long, b: cython.long):
    """
    >>> divmod_long_regular(14000, 700)
    (20, 0)
    >>> divmod_long_regular(4399, 2048)
    (2, 303)
    >>> divmod_long_regular(88321773, 98539211)
    (0, 88321773)
    >>> divmod_long_regular(-99999999, -11111111)
    (9, 0)
    >>> divmod_long_regular(-88888888, -1111111)
    (80, -8)
    >>> divmod_long_regular(-88837244, -110119120)
    (0, -88837244)
    >>> divmod_long_regular(-5000000, 1)
    (-5000000, 0)
    >>> divmod_long_regular(-100190, 17)
    (-5894, 8)
    >>> divmod_long_regular(2014014349, -19)
    (-106000756, -15)
    >>> divmod_long_regular(0, 996007985)
    (0, 0)
    >>> divmod_long_regular(0, -965955)
    (0, 0)

    >>> divmod_long_regular(1380013800, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    return divmod(a,b)
