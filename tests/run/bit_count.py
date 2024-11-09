# mode: run

import cython

def test_bit_count_uchar(value: cython.uchar) -> cython.int:
    """
    >>> test_bit_count_uchar(129)
    2
    """
    return value.bit_count()

def test_bit_count_ushort(value: cython.ushort) -> cython.int:
    """
    >>> test_bit_count_ushort(32769)
    2
    """
    return value.bit_count()

def test_bit_count_uint(value: cython.uint) -> cython.int:
    """
    >>> test_bit_count_uint(32769)
    2
    """
    return value.bit_count()

def test_bit_count_ulong(value: cython.ulong) -> cython.int:
    """
    >>> test_bit_count_ulong(2147483649)
    2
    """
    return value.bit_count()

def test_bit_count_ulonglong(value: cython.ulonglong) -> cython.int:
    """
    >>> test_bit_count_ulonglong(9223372036854775809)
    2
    """
    return value.bit_count()

def test_bit_count_schar(value: cython.schar) -> cython.int:
    """
    >>> test_bit_count_schar(-127)
    7
    >>> test_bit_count_schar(-128)
    1
    """
    return value.bit_count()

def test_bit_count_sshort(value: cython.sshort) -> cython.int:
    """
    >>> test_bit_count_sshort(-32767)
    15
    >>> test_bit_count_sshort(-32768)
    1
    """
    return value.bit_count()

def test_bit_count_sint(value: cython.sint) -> cython.int:
    """
    >>> test_bit_count_sint(-32767)
    15
    >>> test_bit_count_sint(-32768)
    1
    """
    return value.bit_count()

def test_bit_count_slong(value: cython.slong) -> cython.int:
    """
    >>> test_bit_count_slong(-2147483647)
    31
    >>> test_bit_count_slong(-2147483648)
    1
    """
    return value.bit_count()

def test_bit_count_slonglong(value: cython.slonglong) -> cython.int:
    """
    >>> test_bit_count_slonglong(-9223372036854775807)
    63
    >>> test_bit_count_slonglong(-9223372036854775808)
    1
    """
    return value.bit_count()

def test_bit_count_py_int(value: int) -> cython.int:
    """
    >>> test_bit_count_py_int(5)
    2
    >>> test_bit_count_py_int(-9223372036854775807)
    63
    """
    return value.bit_count()

def test_bit_count_py_int_py(value: int):
    """
    >>> test_bit_count_py_int_py(5)
    2
    >>> test_bit_count_py_int_py(-9223372036854775807)
    63
    >>> test_bit_count_py_int_py(18446744073709551617)
    2
    >>> test_bit_count_py_int_py(-18446744073709551617)
    2
    """
    return value.bit_count()
