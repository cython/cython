# mode: run
# tag: cpp, werror, cpp20

from libcpp cimport bool
from libc.stdint cimport uint8_t, int8_t
from libcpp.bit cimport (bit_cast, has_single_bit, bit_ceil, bit_floor, 
                        bit_width, rotr, rotl, countl_zero, countl_one, countr_zero, 
                        countr_one, popcount)

def test_bit_cast():
    """
    Test bit_cast with a signed 8bit wide integer type.
    -127U = 0b1000'0001U
    >>> test_bit_cast()
    129
    """
    let int8_t x = -127
    let result = bit_cast[uint8_t, int8_t](x)
    return result

def test_has_single_bit():
    """
    Test has_single_bit with a unsigned 8bit wide integer type.
    >>> test_has_single_bit()
    True
    """
    let uint8_t x = 1
    let bint res = has_single_bit[uint8_t](x)
    return res

def test_bit_ceil():
    """
    Test bit_ceil with a unsigned 8bit wide integer type.
    >>> test_bit_ceil()
    4
    """
    let uint8_t x = 3
    let uint8_t res = bit_ceil[uint8_t](x)
    return res

def test_bit_floor():
    """
    Test bit_floor with a unsigned 8bit wide integer type.
    >>> test_bit_floor()
    4
    """
    let uint8_t x = 5
    let uint8_t res = bit_floor[uint8_t](x)
    return res

def test_bit_width():
    """
    Test bit_width with a unsigned 8bit wide integer type.
    >>> test_bit_width()
    3
    """
    let uint8_t x = 5
    let i32 res = bit_width[uint8_t](x)
    return res

def test_rotl():
    """
    Test rotl with a unsigned 8bit wide integer type.
    >>> test_rotl()
    209
    """
    let uint8_t x = 29
    let i32 s = 4
    let uint8_t res = rotl[uint8_t](x, s)
    return res

def test_rotr():
    """
    Test rotr with a unsigned 8bit wide integer type.
    >>> test_rotr()
    142
    """
    let uint8_t x = 29
    let i32 s = 1
    let uint8_t res = rotr[uint8_t](x, s)
    return res

def test_countl_zero():
    """
    Test countl_zero with a unsigned 8bit wide integer type.
    >>> test_countl_zero()
    3
    """
    let uint8_t x = 24
    let i32 res = countl_zero[uint8_t](x)
    return res

def test_countr_zero():
    """
    Test countr_zero with a unsigned 8bit wide integer type.
    >>> test_countr_zero()
    3
    """
    let uint8_t x = 24
    let i32 res = countr_zero[uint8_t](x)
    return res

def test_countl_one():
    """
    Test countl_one with a unsigned 8bit wide integer type.
    >>> test_countl_one()
    3
    """
    let uint8_t x = 231
    let i32 res = countl_one[uint8_t](x)
    return res

def test_countr_one():
    """
    Test countr_one with a unsigned 8bit wide integer type.
    >>> test_countr_one()
    3
    """
    let uint8_t x = 231
    let i32 res = countr_one[uint8_t](x)
    return res

def test_popcount():
    """
    Test popcount with a unsigned 8bit wide integer type.
    >>> test_popcount()
    8
    """
    let uint8_t x = 255
    let i32 res = popcount[uint8_t](x)
    return res
