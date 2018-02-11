# mode: run
# ticket: 698

cdef extern from *:
    int INT_MAX
    long LONG_MAX

max_int = INT_MAX
max_long = LONG_MAX
max_long_long = (<object>2) ** (sizeof(long long) * 8 - 1) - 1


cimport cython

def abs_as_name():
    """
    >>> _abs = abs_as_name()
    >>> _abs(-5)
    5
    """
    x = abs
    return x

def py_abs(a):
    """
    >>> py_abs(-5)
    5
    >>> py_abs(-5.5)
    5.5
    """
    return abs(a)

@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = 'abs']")
def sub_abs(int a):
    """
    >>> sub_abs(5)
    (-5, 95)
    >>> sub_abs(105)
    (-105, -5)
    """
    return -abs(a), 100 - abs(a)

@cython.overflowcheck(True)
@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = 'abs']")
def int_abs(int a):
    """
    >>> int_abs(-5) == 5
    True
    >>> int_abs(-5.1) == 5
    True
    >>> int_abs(-max_int-1)     #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    OverflowError: ...
    >>> int_abs(max_int) == abs(max_int)         or (max_int, int_abs(max_int), abs(max_int))
    True
    """
    return abs(a)

@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']")
@cython.test_fail_if_path_exists("//ReturnStatNode//NameNode[@entry.cname = 'abs']",
                                 "//ReturnStatNode//NameNode[@entry.cname = 'labs']")
def uint_abs(unsigned int a):
    """
    >>> uint_abs(max_int) == abs(max_int)         or (max_int, uint_abs(max_int), abs(max_int))
    True
    """
    return abs(a)

@cython.overflowcheck(True)
@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = 'labs']")
def long_abs(long a):
    """
    >>> long_abs(-5) == 5
    True
    >>> long_abs(-5.1) == 5
    True
    >>> long_abs(-max_long-1)     #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    OverflowError: ...
    >>> long_abs(max_long) == abs(max_long)         or (max_long, long_abs(max_long), abs(max_long))
    True
    """
    return abs(a)

@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']")
@cython.test_fail_if_path_exists("//ReturnStatNode//NameNode[@entry.cname = 'abs']",
                                 "//ReturnStatNode//NameNode[@entry.cname = 'labs']")
def ulong_abs(unsigned long a):
    """
    >>> ulong_abs(max_long) == abs(max_long)         or (max_int, ulong_abs(max_long), abs(max_long))
    True
    >>> ulong_abs(max_long + 5) == abs(max_long + 5)         or (max_long + 5, ulong_abs(max_long + 5), abs(max_long + 5))
    True
    """
    return abs(a)

@cython.overflowcheck(True)
@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = '__Pyx_abs_longlong']")
def long_long_abs(long long a):
    """
    >>> long_long_abs(-(2**33)) == 2**33
    True
    >>> long_long_abs(-max_long_long-1)     #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    OverflowError: ...
    >>> long_long_abs(max_long_long) == abs(max_long_long)        or (max_long_long, long_long_abs(max_long_long), abs(max_long_long))
    True
    """
    return abs(a)

@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = 'fabs']")
def double_abs(double a):
    """
    >>> double_abs(-5)
    5.0
    >>> double_abs(-5.5)
    5.5
    """
    return abs(a)

@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = 'fabsf']")
def float_abs(float a):
    """
    >>> float_abs(-5)
    5.0
    >>> float_abs(-5.5)
    5.5
    """
    return abs(a)

@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = '__Pyx_c_abs_double']")
def complex_abs(complex a):
    """
    >>> complex_abs(-5j)
    5.0
    >>> complex_abs(-5.5j)
    5.5
    """
    return abs(a)
