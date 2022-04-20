# mode: run
# tags: cpp, cpp17

from libcpp.algorithm cimport sample
from libcpp.iterator cimport back_inserter
from libcpp.random cimport mt19937
from libcpp.utility cimport move
from libcpp.vector cimport vector


def sample_multiple(population_size, int sample_size):
    """
    >>> sample_multiple(10, 3)
    [3, 5, 6]
    >>> sample_multiple(50, 7)
    [6, 8, 10, 29, 38, 39, 42]
    """
    cdef:
        vector[int] x, y
        int i
        mt19937 rd = mt19937(1)

    [x.push_back(i) for i in range(population_size)]
    sample(x.begin(), x.end(), back_inserter(y), sample_size, move(rd))
    print(y)


def sample_single(population_size):
    """
    >>> sample_single(10)
    5
    """
    cdef:
        vector[int] x
        int i
        mt19937 rd = mt19937(1)

    [x.push_back(i) for i in range(population_size)]
    sample(x.begin(), x.end(), &i, 1, move(rd))
    print(i)
