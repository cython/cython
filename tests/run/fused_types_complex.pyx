# mode: run
# ticket: 5644
# cython: language_level=3
# distutils: define_macros=CYTHON_CCOMPLEX=0

cimport cython

# We used to generate invalid C code for the fused default value assignment
# (int -> complex) with CYTHON_CCOMPLEX=0.

cdef cython.numeric fused_numeric_default(int a = 1, cython.numeric x = 0):
    return x + a


def test_fused_numeric_default(int a, x):
    """
    >>> test_fused_numeric_default(1, 0)
    [1, 1.0, (1+0j)]

    >>> test_fused_numeric_default(1, 2)
    [3, 3.0, (3+0j)]

    >>> test_fused_numeric_default(2, 0)
    [2, 2.0, (2+0j)]

    >>> test_fused_numeric_default(2, 1)
    [3, 3.0, (3+0j)]
    """
    result = []

    if a == 1 and x == 0:
        result.append(fused_numeric_default[int]())
    elif x == 0:
        result.append(fused_numeric_default[int](a))
    elif a == 1:
        result.append(fused_numeric_default[int](1, x))
    else:
        result.append(fused_numeric_default[int](a, x))

    if a == 1 and x == 0:
        result.append(fused_numeric_default[float]())
    elif x == 0:
        result.append(fused_numeric_default[float](a))
    elif a == 1:
        result.append(fused_numeric_default[float](1, x))
    else:
        result.append(fused_numeric_default[float](a, x))

    if a == 1 and x == 0:
        result.append(fused_numeric_default[cython.doublecomplex]())
    elif x == 0:
        result.append(fused_numeric_default[cython.doublecomplex](a))
    elif a == 1:
        result.append(fused_numeric_default[cython.doublecomplex](1, x))
    else:
        result.append(fused_numeric_default[cython.doublecomplex](a, x))

    return result
