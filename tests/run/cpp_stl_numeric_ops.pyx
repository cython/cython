# mode: run
# tag: cpp, werror, cpp11

from libcpp.numeric cimport inner_product, iota, accumulate
from libcpp.vector cimport vector

def test_inner_product(vector[int] v1, vector[int] v2, int init):
    """
    Test inner_product with integer values.

    >>> test_inner_product([1, 2, 3], [1, 2, 3], 1)
    15
    """
    return inner_product(v1.begin(), v1.end(), v2.begin(), init)


def test_inner_product_with_zero(vector[int] v1, vector[int] v2, int init):
    """
    Test inner_product with a zero value in the container.

    >>> test_inner_product_with_zero([1, 2, 0], [1, 1, 1], 0)
    3
    """
    return inner_product(v1.begin(), v1.end(), v2.begin(), init)

def test_iota(vector[int] v, int value):
    """
    Test iota with beginning value of 0.

    >>> test_iota(range(6), 0)
    [0, 1, 2, 3, 4, 5]
    """
    iota(v.begin(), v.end(), value)
    return v

def test_iota_negative_init(vector[int] v, int value):
    """
    Test iota with a negative beginning value.

    >>> test_iota_negative_init(range(7), -4)
    [-4, -3, -2, -1, 0, 1, 2]
    """
    iota(v.begin(), v.end(), value)
    return v

cdef int subtract_integers(int lhs, int rhs):
    return lhs - rhs

def test_accumulate_with_subtraction(vector[int] v, int init):
    """
    Test accumulate with subtraction. Note that accumulate is a fold-left operation.
     0 - 1 = -1
    -1 - 2 = -3
    -3 - 3 = -6

    >>> test_accumulate_with_subtraction([1, 2, 3], 0)
    -6
    """
    return accumulate(v.begin(), v.end(), init, subtract_integers)


