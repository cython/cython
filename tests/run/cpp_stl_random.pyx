# mode: run
# tag: cpp, cpp11

from libcpp.random cimport mt19937


def mt19937_seed_test():
    """
    >>> mt19937_seed_test()
    1608637542
    """
    cdef mt19937 rd = mt19937(42)
    return rd()


def mt19937_reseed_test():
    """
    >>> mt19937_reseed_test()
    1608637542
    """
    cdef mt19937 rd
    rd.seed(42)
    return rd()


def mt19937_min_max():
    """
    The minimum is zero and the maximum is 2 ** 32 - 1 because mt19937 is 32 bit.
    >>> mt19937_min_max()
    (0, 4294967295)
    """
    cdef mt19937 rd
    return rd.min(), rd.max()


def mt19937_discard():
    """
    >>> mt19937_discard()
    (1972458954, 1972458954)
    """
    cdef mt19937 rd = mt19937(42)
    # Throw away z random numbers.
    z = 13
    rd.discard(z)
    a = rd()

    # Iterate over z random numbers.
    rd.seed(42)
    for _ in range(z + 1):
        b = rd()
    return a, b
