# mode: run

# Test longintrepr declarations by implementing a simple function

from cpython.longintrepr cimport *
cimport cython

@cython.cdivision(true)
def lshift(i64 a, u64 n):
    """
    Return a * 2^n as Python long.

    >>> print(lshift(3, 1))
    6
    >>> print(lshift(1, 30))
    1073741824
    >>> print(lshift(-12345, 115))
    512791237748899576593671817473776680960
    >>> print(-12345 << 115)
    -512791237748899576593671817473776680960
    >>> [i for i in range(100) if (65535 << i) != lshift(65535, i)]
    []
    >>> print(lshift(0, 12345))
    0
    >>> print(lshift(2**62, 0))   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError...
    """
    if not a:
        return _PyLong_New(0)
    cdef u64 apos = a if a > 0 else -a
    if (apos >> 1) >= <u64>PyLong_BASE:
        raise OverflowError

    cdef u64 index = n // PyLong_SHIFT
    cdef u64 shift = n % PyLong_SHIFT

    cdef digit d = apos
    cdef digit low = (d << shift) & PyLong_MASK
    cdef digit high = (d >> (PyLong_SHIFT - shift))

    if high == 0:
        ret = _PyLong_New(index + 1)
        ret.ob_digit[index] = low
    else:
        ret = _PyLong_New(index + 2)
        ret.ob_digit[index] = low
        ret.ob_digit[index + 1] = high

    while index >= 1:
        index -= 1
        ret.ob_digit[index] = 0

    return ret
