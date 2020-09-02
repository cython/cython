
cdef extern from *:
    ctypedef long long int128_t "__int128_t"
    ctypedef unsigned long long uint128_t "__uint128_t"


def bigint(x):
    print(str(x).rstrip('L'))


def unsigned_conversion(x):
    """
    >>> bigint(unsigned_conversion(0))
    0
    >>> bigint(unsigned_conversion(2))
    2

    >>> unsigned_conversion(-2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    OverflowError: can't convert negative value to ...uint128_t
    >>> unsigned_conversion(-2**120)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    OverflowError: can't convert negative value to ...uint128_t
    >>> unsigned_conversion(-2**127)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    OverflowError: can't convert negative value to ...uint128_t
    >>> unsigned_conversion(-2**128)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    OverflowError: can't convert negative value to ...uint128_t

    >>> bigint(unsigned_conversion(2**20))
    1048576
    >>> bigint(unsigned_conversion(2**30-1))
    1073741823
    >>> bigint(unsigned_conversion(2**30))
    1073741824
    >>> bigint(unsigned_conversion(2**30+1))
    1073741825

    >>> bigint(2**60)
    1152921504606846976
    >>> bigint(unsigned_conversion(2**60-1))
    1152921504606846975
    >>> bigint(unsigned_conversion(2**60))
    1152921504606846976
    >>> bigint(unsigned_conversion(2**60+1))
    1152921504606846977
    >>> bigint(2**64)
    18446744073709551616
    >>> bigint(unsigned_conversion(2**64))
    18446744073709551616

    >>> bigint(2**120)
    1329227995784915872903807060280344576
    >>> bigint(unsigned_conversion(2**120))
    1329227995784915872903807060280344576
    >>> bigint(2**128-1)
    340282366920938463463374607431768211455
    >>> bigint(unsigned_conversion(2**128-1))
    340282366920938463463374607431768211455
    >>> bigint(unsigned_conversion(2**128))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    OverflowError: ... too big to convert
    """
    cdef uint128_t n = x
    return n


def signed_conversion(x):
    """
    >>> bigint(signed_conversion(0))
    0
    >>> bigint(signed_conversion(2))
    2
    >>> bigint(signed_conversion(-2))
    -2

    >>> bigint(signed_conversion(2**20))
    1048576
    >>> bigint(signed_conversion(2**32))
    4294967296
    >>> bigint(2**64)
    18446744073709551616
    >>> bigint(signed_conversion(2**64))
    18446744073709551616
    >>> bigint(signed_conversion(-2**64))
    -18446744073709551616

    >>> bigint(2**118)
    332306998946228968225951765070086144
    >>> bigint(signed_conversion(2**118))
    332306998946228968225951765070086144
    >>> bigint(signed_conversion(-2**118))
    -332306998946228968225951765070086144

    >>> bigint(2**120)
    1329227995784915872903807060280344576
    >>> bigint(signed_conversion(2**120))
    1329227995784915872903807060280344576
    >>> bigint(signed_conversion(-2**120))
    -1329227995784915872903807060280344576

    >>> bigint(2**127-1)
    170141183460469231731687303715884105727
    >>> bigint(signed_conversion(2**127-2))
    170141183460469231731687303715884105726
    >>> bigint(signed_conversion(2**127-1))
    170141183460469231731687303715884105727
    >>> bigint(signed_conversion(2**127))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    OverflowError: ... too big to convert
    >>> bigint(signed_conversion(-2**127))
    -170141183460469231731687303715884105728
    >>> bigint(signed_conversion(-2**127-1))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    OverflowError: ... too big to convert
    """
    cdef int128_t n = x
    return n


def get_int_distribution(shuffle=True):
    """
    >>> L = get_int_distribution()
    >>> bigint(L[0])
    682
    >>> bigint(L[ len(L) // 2 ])
    3002399751580330
    >>> bigint(L[-1])
    13195544127517395320358043648
    >>> len(L)
    252000
    """
    # Large integers that cover 1-4 (30 bits) or 1-7 (15 bits) PyLong digits.
    ints = [int((2.0 ** (n/1000.)) / 3) for n in range(11 * 1000, 95 * 1000)]
    return ints * 3  # longer list, but keeps median in the middle


def intsum(L):
    """
    >>> L = get_int_distribution()
    >>> bigint(intsum(L))
    57131233826607488945110474209519
    >>> bigint(sum(L))
    57131233826607488945110474209519

    >>> from random import shuffle
    >>> shuffle(L)
    >>> bigint(intsum(L))
    57131233826607488945110474209519
    """
    cdef uint128_t i, x = 0
    for i in L:
        x += i
    return x


def intxor(L):
    """
    >>> L = get_int_distribution()
    >>> bigint(intxor(L))
    11140796789428055795371202119
    >>> bigint(intxor(L * 2))
    0
    >>> import operator
    >>> from functools import reduce
    >>> bigint(reduce(operator.xor, L))
    11140796789428055795371202119
    >>> bigint(reduce(operator.xor, L * 2))
    0

    >>> from random import shuffle
    >>> shuffle(L)
    >>> bigint(intxor(L))
    11140796789428055795371202119
    >>> bigint(intxor(L * 2))
    0
    """
    cdef uint128_t i, x = 0
    for i in L:
        x ^= i
    return x
