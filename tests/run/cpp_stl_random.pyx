# mode: run
# tag: cpp, cpp11

from libcpp.random cimport mt19937, mt19937_64


def mt19937_seed_test():
    """
    >>> print(mt19937_seed_test())
    1608637542
    """
    cdef mt19937 gen = mt19937(42)
    return gen()


def mt19937_reseed_test():
    """
    >>> print(mt19937_reseed_test())
    1608637542
    """
    cdef mt19937 gen
    gen.seed(42)
    return gen()


def mt19937_min_max():
    """
    >>> x, y = mt19937_min_max()
    >>> print(x)
    0
    >>> print(y)  # 2 ** 32 - 1 because mt19937 is 32 bit.
    4294967295
    """
    cdef mt19937 gen
    return gen.min(), gen.max()


def mt19937_discard(z):
    """
    >>> x, y = mt19937_discard(13)
    >>> print(x)
    1972458954
    >>> print(y)
    1972458954
    """
    cdef mt19937 gen = mt19937(42)
    # Throw away z random numbers.
    gen.discard(z)
    a = gen()

    # Iterate over z random numbers.
    gen.seed(42)
    for _ in range(z + 1):
        b = gen()
    return a, b


def mt19937_64_seed_test():
    """
    >>> print(mt19937_64_seed_test())
    13930160852258120406
    """
    cdef mt19937_64 gen = mt19937_64(42)
    return gen()


def mt19937_64_reseed_test():
    """
    >>> print(mt19937_64_reseed_test())
    13930160852258120406
    """
    cdef mt19937_64 gen
    gen.seed(42)
    return gen()


def mt19937_64_min_max():
    """
    >>> x, y = mt19937_64_min_max()
    >>> print(x)
    0
    >>> print(y)  # 2 ** 64 - 1 because mt19937_64 is 64 bit.
    18446744073709551615
    """
    cdef mt19937_64 gen
    return gen.min(), gen.max()


def mt19937_64_discard(z):
    """
    >>> x, y = mt19937_64_discard(13)
    >>> print(x)
    11756813601242511406
    >>> print(y)
    11756813601242511406
    """
    cdef mt19937_64 gen = mt19937_64(42)
    # Throw away z random numbers.
    gen.discard(z)
    a = gen()

    # Iterate over z random numbers.
    gen.seed(42)
    for _ in range(z + 1):
        b = gen()
    return a, b
