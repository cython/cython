# mode: run
# ticket: 698

cdef extern from *:
    int INT_MAX
    long LONG_MAX

max_int = INT_MAX
max_long = LONG_MAX
max_long_long = 2 ** (sizeof(long long) * 8 - 1) - 1


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
                                "//ReturnStatNode//NameNode[@entry.cname = '__Pyx_abs_int']")
def int_abs(int a):
    """
    >>> int_abs(-5) == 5
    True
    >>> int_abs(-5.1) == 5
    True
    >>> long_abs(-max_int-1) > 0
    True
    >>> int_abs(-max_int-1) == abs(-max_int-1)
    True
    >>> int_abs(max_int) == abs(max_int)
    True
    """
    return abs(a)

@cython.test_assert_path_exists("//ReturnStatNode//NameNode[@entry.name = 'abs']",
                                "//ReturnStatNode//NameNode[@entry.cname = '__Pyx_abs_long']")
def long_abs(long a):
    """
    >>> long_abs(-5) == 5
    True
    >>> long_abs(-5.1) == 5
    True
    >>> long_abs(-max_long-1) > 0
    True
    >>> long_abs(-max_long-1) == abs(-max_long-1)
    True
    >>> long_abs(max_long) == abs(max_long)
    True
    """
    return abs(a)

def long_long_abs(long long a):
    """
    >>> long_long_abs(-(2**33)) == 2**33
    True
    >>> long_long_abs(-max_long_long-1) > 0
    True
    >>> long_long_abs(-max_long_long-1) == abs(-max_long_long-1)
    True
    >>> long_long_abs(max_long_long) == abs(max_long_long)
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
