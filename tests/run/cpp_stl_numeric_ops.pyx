# mode: run
# tag: cpp, werror, cpp11

from libcpp.numeric cimport inner_product, iota, accumulate, adjacent_difference, partial_sum
from libcpp.vector cimport vector
from libcpp cimport bool

# Subtracts two integers.
cdef int subtract_integers(int lhs, int rhs):
    return lhs - rhs

# Adds two integers.
cdef int add_integers(int lhs, int rhs):
    return lhs + rhs

# Multiplies two integers.
cdef int multiply_integers(int lhs, int rhs):
    return lhs * rhs

# Determines equality for two integers.
# If lhs == rhs, returns true. Returns false otherwise.
cdef bool is_equal(int lhs, int rhs):
    return lhs == rhs

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

def test_inner_product_with_bin_op(vector[int] v1, vector[int] v2, int init):
    """
    Test inner_product with two binary operations. In this case,
    Looks at number of pairwise matches between v1 and v2.
    [5, 1, 2, 3, 4]
    [5, 4, 2, 3, 1]
    There are 3 matches (5, 2, 3). So, 1 + 1 + 1 = 3.

    >>> test_inner_product_with_bin_op([5, 1, 2, 3, 4], [5, 4, 2, 3, 1], 0)
    3
    """
    return inner_product(v1.begin(), v1.end(), v2.begin(), init, add_integers, is_equal)

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

def test_accumulate(vector[int] v, int init):
    """
    Test accumulate.
     0 + 1 = 1
     1 + 2 = 3
     3 + 3 = 6
    >>> test_accumulate([1, 2, 3], 0)
    6
    """
    return accumulate(v.begin(), v.end(), init)

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

def test_adjacent_difference(vector[int] v):
    """
    Test adjacent_difference with integer values.
    2 - 0,   -> 2
    4 - 2,   -> 2
    6 - 4,   -> 2
    8 - 6,   -> 2
    10 - 8,  -> 2
    12 - 10  -> 2
    >>> test_adjacent_difference([2, 4, 6, 8, 10, 12])
    [2, 2, 2, 2, 2, 2]
    """
    adjacent_difference(v.begin(), v.end(), v.begin())
    return v

def test_adjacent_difference_with_bin_op(vector[int] v):
    """
    Test adjacent_difference with a binary operation.
    0 + 1 -> 1
    1 + 2 -> 3
    2 + 4 -> 6
    4 + 5 -> 9
    5 + 6 -> 11
    >>> test_adjacent_difference_with_bin_op([1, 2, 4, 5, 6])
    [1, 3, 6, 9, 11]
    """
    adjacent_difference(v.begin(), v.end(), v.begin(), add_integers)
    return v

def test_partial_sum(vector[int] v):
    """
    Test partial_sum with integer values.
    2 + 0   -> 2
    2 + 2   -> 4
    4 + 2   -> 6
    6 + 2   -> 8
    8 + 2   -> 10
    10 + 2  -> 12
    >>> test_partial_sum([2, 2, 2, 2, 2, 2])
    [2, 4, 6, 8, 10, 12]
    """
    partial_sum(v.begin(), v.end(), v.begin())
    return v

def test_partial_sum_with_bin_op(vector[int] v):
    """
    Test partial_sum with a binary operation.
    Using multiply_integers, partial_sum will calculate the first 5 powers of 2.
    >>> test_partial_sum_with_bin_op([2, 2, 2, 2, 2])
    [2, 4, 8, 16, 32]
    """
    partial_sum(v.begin(), v.end(), v.begin(), multiply_integers)
    return v
