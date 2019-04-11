# mode: run
# tag: multiply

import sys
IS_PY2 = sys.version_info[0] < 3


def print_long(x):
    if IS_PY2:
        x = str(x).rstrip('L')
    print(x)


def mul_10_obj(x):
    """
    >>> mul_10_obj(0)
    0
    >>> mul_10_obj(10)
    100
    >>> mul_10_obj(-10)
    -100
    >>> 10 * (2**14)
    163840
    >>> mul_10_obj(2**14)
    163840
    >>> mul_10_obj(-2**14)
    -163840
    >>> print_long(10 * (2**29))
    5368709120
    >>> print_long(mul_10_obj(2**29))
    5368709120
    >>> print_long(mul_10_obj(-2**29))
    -5368709120
    >>> print_long(10 * (2**30))
    10737418240
    >>> print_long(mul_10_obj(2**30))
    10737418240
    >>> print_long(mul_10_obj(-2**30))
    -10737418240
    >>> print_long(10 * (2**63))
    92233720368547758080
    >>> print_long(mul_10_obj(2**63))
    92233720368547758080
    >>> print_long(mul_10_obj(-2**63))
    -92233720368547758080
    >>> print_long(10 * (2**128))
    3402823669209384634633746074317682114560
    >>> print_long(mul_10_obj(2**128))
    3402823669209384634633746074317682114560
    >>> print_long(mul_10_obj(-2**128))
    -3402823669209384634633746074317682114560
    """
    result = 10 * x
    return result


def mul_obj_10(x):
    """
    >>> mul_obj_10(0)
    0
    >>> mul_obj_10(10)
    100
    >>> mul_obj_10(-10)
    -100
    >>> 10 * (2**14)
    163840
    >>> mul_obj_10(2**14)
    163840
    >>> mul_obj_10(-2**14)
    -163840
    >>> print_long(10 * (2**29))
    5368709120
    >>> print_long(mul_obj_10(2**29))
    5368709120
    >>> print_long(mul_obj_10(-2**29))
    -5368709120
    >>> print_long(10 * (2**30))
    10737418240
    >>> print_long(mul_obj_10(2**30))
    10737418240
    >>> print_long(mul_obj_10(-2**30))
    -10737418240
    >>> print_long(10 * (2**63))
    92233720368547758080
    >>> print_long(mul_obj_10(2**63))
    92233720368547758080
    >>> print_long(mul_obj_10(-2**63))
    -92233720368547758080
    >>> print_long(10 * (2**128))
    3402823669209384634633746074317682114560
    >>> print_long(mul_obj_10(2**128))
    3402823669209384634633746074317682114560
    >>> print_long(mul_obj_10(-2**128))
    -3402823669209384634633746074317682114560
    """
    result = x * 10
    return result


def mul_bigint_obj(x):
    """
    >>> mul_bigint_obj(0)
    0
    >>> print_long(mul_bigint_obj(1))
    536870912
    >>> print_long(mul_bigint_obj(2))
    1073741824
    >>> print_long(mul_bigint_obj(2**29))
    288230376151711744
    >>> print_long(mul_bigint_obj(-2**29))
    -288230376151711744
    >>> print_long(mul_bigint_obj(2**30))
    576460752303423488
    >>> print_long(mul_bigint_obj(-2**30))
    -576460752303423488
    >>> print_long(mul_bigint_obj(2**59))
    309485009821345068724781056
    >>> print_long(mul_bigint_obj(-2**59))
    -309485009821345068724781056
    """
    result = (2**29) * x
    return result


def mul_obj_float(x):
    """
    >>> mul_obj_float(-0.0)
    -0.0
    >>> mul_obj_float(0)
    0.0
    >>> mul_obj_float(1.0)
    2.0
    >>> mul_obj_float(-2.0)
    -4.0
    >>> mul_obj_float(-0.5)
    -1.0
    """
    result = x * 2.0
    return result


def mul_float_obj(x):
    """
    >>> mul_float_obj(0)
    0.0
    >>> mul_float_obj(2)
    4.0
    >>> mul_float_obj(-2)
    -4.0
    >>> 2.0 * (2**30-1)
    2147483646.0
    >>> mul_float_obj(2**30-1)
    2147483646.0
    >>> mul_float_obj(-(2**30-1))
    -2147483646.0
    >>> mul_float_obj(-0.0)
    -0.0
    >>> mul_float_obj(1.0)
    2.0
    >>> mul_float_obj(-2.0)
    -4.0
    >>> mul_float_obj(-0.5)
    -1.0
    """
    result = 2.0 * x
    return result
