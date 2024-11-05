# mode: run

import cython


@cython.cfunc
@cython.returns(cython.uchar)
def bit_count_uchar(value: cython.uchar):
    return value.bit_count()


@cython.cfunc
@cython.returns(cython.short)
def bit_count_ushort(value: cython.ushort):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_uint(value: cython.uint):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_ulong(value: cython.ulong):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_ulonglong(value: cython.ulonglong):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.uchar)
def bit_count_schar(value: cython.schar):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.short)
def bit_count_sshort(value: cython.sshort):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_sint(value: cython.sint):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_slong(value: cython.slong):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_slonglong(value: cython.slonglong):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_py_int(value):
    return value.bit_count()

@cython.cfunc
def bit_count_py_int_py(value):
    return value.bit_count()


def test_bit_count_uchar(value):
    """
    >>> test_bit_count_uchar(129)
    2
    """
    return bit_count_uchar(value)

def test_bit_count_ushort(value):
    """
    >>> test_bit_count_ushort(32769)
    2
    """
    return bit_count_ushort(value)

def test_bit_count_uint(value):
    """
    >>> test_bit_count_uint(32769)
    2
    """
    return bit_count_uint(value)

def test_bit_count_ulong(value):
    """
    >>> test_bit_count_ulong(2147483649)
    2
    """
    return bit_count_ulong(value)

def test_bit_count_ulonglong(value):
    """
    >>> test_bit_count_ulonglong(9223372036854775809)
    2
    """
    return bit_count_ulonglong(value)

def test_bit_count_schar(value):
    """
    >>> test_bit_count_schar(-127)
    7
    >>> test_bit_count_schar(-128)
    1
    """
    return bit_count_schar(value)

def test_bit_count_sshort(value):
    """
    >>> test_bit_count_sshort(-32767)
    15
    >>> test_bit_count_sshort(-32768)
    1
    """
    return bit_count_sshort(value)

def test_bit_count_sint(value):
    """
    >>> test_bit_count_sint(-32767)
    15
    >>> test_bit_count_sint(-32768)
    1
    """
    return bit_count_sint(value)

def test_bit_count_slong(value):
    """
    >>> test_bit_count_slong(-2147483647)
    31
    >>> test_bit_count_slong(-2147483648)
    1
    """
    return bit_count_slong(value)

def test_bit_count_slonglong(value):
    """
    >>> test_bit_count_slonglong(-9223372036854775807)
    63
    >>> test_bit_count_slonglong(-9223372036854775808)
    1
    """
    return bit_count_slonglong(value)

def test_bit_count_py_int(value):
    """
    >>> test_bit_count_py_int(5)
    2
    >>> test_bit_count_py_int(-9223372036854775807)
    63
    """
    return bit_count_py_int(value)

def test_bit_count_py_int_py(value):
    """
    >>> test_bit_count_py_int_py(5)
    2
    >>> test_bit_count_py_int_py(-9223372036854775807)
    63
    """
    return bit_count_py_int_py(value)
