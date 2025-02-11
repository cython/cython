# mode: run
# tag: cpp, cpp17, no-cpp-locals

from libcpp.algorithm cimport sample
from libcpp.iterator cimport back_inserter
from libcpp.random cimport mt19937
from libcpp.utility cimport move
from libcpp.vector cimport vector


def sample_multiple(population_size, int sample_size):
    """
    >>> sample = sample_multiple(10, 7)
    >>> len(sample), len(set(sample))  # Check sampling without replacement.
    (7, 7)
    """
    cdef:
        vector[int] x, y
        int i
        mt19937 rd = mt19937(1)

    for i in range(population_size):
        x.push_back(i)
    sample(x.begin(), x.end(), back_inserter(y), sample_size, move(rd))
    return y


def sample_single(population_size):
    """
    >>> 0 <= sample_single(10) < 10
    True
    """
    cdef:
        vector[int] x
        int i
        mt19937 rd = mt19937(1)

    for i in range(population_size):
        x.push_back(i)
    sample(x.begin(), x.end(), &i, 1, move(rd))
    return i
