# mode: run
# tag: cpp, cpp11

from libcpp.random cimport mt19937, uniform_int_distribution, uniform_real_distribution, \
    bernoulli_distribution, binomial_distribution, geometric_distribution


def mt19937_seed_test():
    """
    >>> print(mt19937_seed_test())
    1608637542
    """
    cdef mt19937 rd = mt19937(42)
    return rd()


def mt19937_reseed_test():
    """
    >>> print(mt19937_reseed_test())
    1608637542
    """
    cdef mt19937 rd
    rd.seed(42)
    return rd()


def mt19937_min_max():
    """
    >>> x, y = mt19937_min_max()
    >>> print(x)
    0
    >>> print(y)  # 2 ** 32 - 1 because mt19937 is 32 bit.
    4294967295
    """
    cdef mt19937 rd
    return rd.min(), rd.max()


def mt19937_discard(z):
    """
    >>> x, y = mt19937_discard(13)
    >>> print(x)
    1972458954
    >>> print(y)
    1972458954
    """
    cdef mt19937 rd = mt19937(42)
    # Throw away z random numbers.
    rd.discard(z)
    a = rd()

    # Iterate over z random numbers.
    rd.seed(42)
    for _ in range(z + 1):
        b = rd()
    return a, b


def uniform_int_distribution_sample(a, b):
    """
    >>> uniform_int_distribution_sample(0, 0)
    0
    >>> uniform_int_distribution_sample(0, 1) < 2
    True
    """
    cdef uniform_int_distribution[int] dist = uniform_int_distribution[int](a, b)
    return dist(mt19937(42))


def uniform_real_distribution_sample(a, b):
    """
    >>> uniform_real_distribution_sample(0, 0)
    0.0
    >>> x = uniform_real_distribution_sample(0, 5)
    >>> 0 < x and x < 5
    True
    """
    cdef uniform_real_distribution[float] dist = uniform_real_distribution[float](a, b)
    return dist(mt19937(42))


def bernoulli_distribution_sample(proba):
    """
    >>> bernoulli_distribution_sample(0)
    False
    >>> bernoulli_distribution_sample(1)
    True
    """
    cdef bernoulli_distribution dist = bernoulli_distribution(proba)
    return dist(mt19937(42))


def binomial_distribution_sample(n, proba):
    """
    >>> binomial_distribution_sample(10, 0)
    0
    >>> binomial_distribution_sample(10, 1)
    10
    >>> x = binomial_distribution_sample(100, 0.5)
    >>> 0 < x and x < 100  # Passes with high probability.
    True
    """
    cdef binomial_distribution[int] dist = binomial_distribution[int](n, proba)
    return dist(mt19937(42))


def geometric_distribution_sample(proba):
    """
    >>> geometric_distribution_sample(1)
    0
    >>> geometric_distribution_sample(1e-5) > 100  # Passes with high probability.
    True
    """
    cdef geometric_distribution[int] dist = geometric_distribution[int](proba)
    return dist(mt19937(42))
