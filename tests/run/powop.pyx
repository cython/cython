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


class I(int):
    """
    Copied from CPython's test_descr.py

    >>> I(2) ** I(3)
    I(8)
    >>> 2 ** I(3)
    I(8)
    >>> I(3).pow2()
    I(8)
    """
    def __repr__(self):
        return 'I(%s)' % int(self)
    def __pow__(self, other, mod=None):
        if mod is None:
            return I(pow(int(self), int(other)))
        else:
            return I(pow(int(self), int(other), int(mod)))
    def __rpow__(self, other, mod=None):
        if mod is None:
            return I(pow(int(other), int(self), mod))
        else:
            return I(pow(int(other), int(self), int(mod)))

    def pow2(self):
        return 2 ** self


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
    >>> print(repr(optimised_pow2(31)).rstrip('L'))
    2147483648
    >>> print(repr(optimised_pow2(32)).rstrip('L'))
    4294967296
    >>> print(repr(optimised_pow2(60)).rstrip('L'))
    1152921504606846976
    >>> print(repr(optimised_pow2(63)).rstrip('L'))
    9223372036854775808
    >>> print(repr(optimised_pow2(64)).rstrip('L'))
    18446744073709551616
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


def optimised_pow2_inplace(n):
    """
    >>> optimised_pow2_inplace(0)
    1
    >>> optimised_pow2_inplace(1)
    2
    >>> optimised_pow2_inplace(10)
    1024
    >>> optimised_pow2_inplace(30)
    1073741824
    >>> print(repr(optimised_pow2_inplace(32)).rstrip('L'))
    4294967296
    >>> print(repr(optimised_pow2_inplace(100)).rstrip('L'))
    1267650600228229401496703205376
    >>> optimised_pow2_inplace(30000) == 2 ** 30000
    True
    >>> optimised_pow2_inplace(-1)
    0.5
    >>> optimised_pow2_inplace(0.5) == 2 ** 0.5
    True
    >>> optimised_pow2_inplace('test')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'str'
    """
    x = 2
    x **= n
    return x
