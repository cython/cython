# mode: run

import cython


@cython.cfunc
@cython.returns(cython.unsigned_char)
def bit_count_unsigned_char(value: cython.unsigned_char):
    return value.bit_count()


@cython.cfunc
@cython.returns(cython.short)
def bit_count_unsigned_short(value: cython.unsigned_short):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_unsigned_int(value: cython.unsigned_int):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_unsigned_long(value: cython.unsigned_long):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_unsigned_longlong(value: cython.unsigned_longlong):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.unsigned_char)
def bit_count_signed_char(value: cython.signed_char):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.short)
def bit_count_signed_short(value: cython.signed_short):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_signed_int(value: cython.signed_int):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_signed_long(value: cython.signed_long):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_signed_longlong(value: cython.signed_longlong):
    return value.bit_count()

@cython.cfunc
@cython.returns(cython.int)
def bit_count_py_int(value):
    return value.bit_count()

@cython.cfunc
def bit_count_py_int_py(value):
    return value.bit_count()


def test_bit_count_unsigned_char(value):
    """
    >>> test_bit_count_unsigned_char(129)
    2
    """
    return bit_count_unsigned_char(value)

def test_bit_count_unsigned_short(value):
    """
    >>> test_bit_count_unsigned_short(32769)
    2
    """
    return bit_count_unsigned_short(value)

def test_bit_count_unsigned_int(value):
    """
    >>> test_bit_count_unsigned_int(32769)
    2
    """
    return bit_count_unsigned_int(value)

def test_bit_count_unsigned_long(value):
    """
    >>> test_bit_count_unsigned_long(2147483649)
    2
    """
    return bit_count_unsigned_long(value)

def test_bit_count_unsigned_longlong(value):
    """
    >>> test_bit_count_unsigned_longlong(9223372036854775809)
    2
    """
    return bit_count_unsigned_longlong(value)

def test_bit_count_signed_char(value):
    """
    >>> test_bit_count_signed_char(-127)
    7
    >>> test_bit_count_signed_char(-128)
    1
    """
    return bit_count_signed_char(value)

def test_bit_count_signed_short(value):
    """
    >>> test_bit_count_signed_short(-32767)
    15
    >>> test_bit_count_signed_short(-32768)
    1
    """
    return bit_count_signed_short(value)

def test_bit_count_signed_int(value):
    """
    >>> test_bit_count_signed_int(-32767)
    15
    >>> test_bit_count_signed_int(-32768)
    1
    """
    return bit_count_signed_int(value)

def test_bit_count_signed_long(value):
    """
    >>> test_bit_count_signed_long(-2147483647)
    31
    >>> test_bit_count_signed_long(-2147483648)
    1
    """
    return bit_count_signed_long(value)

def test_bit_count_signed_longlong(value):
    """
    >>> test_bit_count_signed_longlong(-9223372036854775807)
    63
    >>> test_bit_count_signed_longlong(-9223372036854775808)
    1
    """
    return bit_count_signed_longlong(value)

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
