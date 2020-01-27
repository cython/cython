# mode: run
# tag: cpp, werror, cpp11

from cython.operator cimport dereference as deref
from libcpp.numeric cimport inner_product
from libcpp.vector cimport vector

def test_inner_product(vector[int] v1, vector[int] v2, int init):
    """
    Test inner_product with integer values.

    >>> test_inner_product([1,2,3], [1,2,3], 1)
    15
    """
    return inner_product(v1.begin(), v1.end(), v2.begin(), init);


def test_inner_product_with_zero(vector[int] v1, vector[int] v2, int init):
    """
    Test inner_product with a zero value in the container.

    >>> test_inner_product_with_zero([1,2,0], [1,1,1], 0)
    3
    """
    return inner_product(v1.begin(), v1.end(), v2.begin(), init);

