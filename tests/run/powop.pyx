def f(obj2, obj3):
    """
    >>> f(1.0, 2.95)[0] == f(1.0, 2.95)[1]
    True
    """
    cdef float flt1, flt2, flt3
    flt2, flt3 = obj2, obj3

    flt1 = flt2 ** flt3
    obj1 = obj2 ** obj3
    return flt1, obj1


def g(i):
    """
    >>> g(4)
    1024
    """
    return i ** 5


def h(i):
    """
    >>> h(4)
    625
    """
    return 5 ** i


def constant_py():
    """
    >>> constant_py() == 2 ** 10
    True
    """
    result = (<object>2) ** 10
    return result


def constant_long():
    """
    >>> constant_long() == 2 ** 36
    True
    """
    result = (<object>2L) ** 36
    return result


def small_int_pow(long s):
    """
    >>> small_int_pow(3)
    (1, 3, 9, 27, 81)
    >>> small_int_pow(-5)
    (1, -5, 25, -125, 625)
    """
    return s**0, s**1, s**2, s**3, s**4


def int_pow(short a, short b):
    """
    >>> int_pow(7, 2)
    49
    >>> int_pow(5, 3)
    125
    >>> int_pow(2, 10)
    1024
    """
    return a**b


def optimised_pow2(n):
    """
    >>> optimised_pow2(0)
    1
    >>> optimised_pow2(1)
    2
    >>> optimised_pow2(10)
    1024
    >>> optimised_pow2(30)
    1073741824
    >>> print(repr(optimised_pow2(32)).rstrip('L'))
    4294967296
    >>> print(repr(optimised_pow2(100)).rstrip('L'))
    1267650600228229401496703205376
    >>> optimised_pow2(30000) == 2 ** 30000
    True
    >>> optimised_pow2(-1)
    0.5
    >>> optimised_pow2(0.5) == 2 ** 0.5
    True
    >>> optimised_pow2('test')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'str'
    """
    if isinstance(n, (int, long)) and 0 <= n < 1000:
        assert isinstance(2.0 ** n, float), 'float %s' % n
        assert isinstance(2 ** n, (int, long)), 'int %s' % n
    return 2 ** n
