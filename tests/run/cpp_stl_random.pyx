# mode: run
# tag: cpp, cpp11

from libcpp.random cimport mt19937, random_device, uniform_int_distribution, \
    uniform_real_distribution, bernoulli_distribution, binomial_distribution, \
    geometric_distribution, negative_binomial_distribution, poisson_distribution


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


ctypedef fused any_dist:
    uniform_int_distribution[int]
    uniform_real_distribution[double]
    bernoulli_distribution
    binomial_distribution[int]
    geometric_distribution[int]
    negative_binomial_distribution[int]
    poisson_distribution[int]


cdef sample_or_range(any_dist dist, bint sample):
    cdef random_device rd
    if sample:
        return dist(mt19937(rd()))
    else:
        return dist.min(), dist.max()


def uniform_int_distribution_test(a, b, sample=True):
    """
    >>> uniform_int_distribution_test(0, 0)
    0
    >>> uniform_int_distribution_test(0, 1) < 2
    True
    >>> uniform_int_distribution_test(5, 9, False)
    (5, 9)
    """
    cdef uniform_int_distribution[int] dist = uniform_int_distribution[int](a, b)
    return sample_or_range[uniform_int_distribution[int]](dist, sample)


def uniform_real_distribution_test(a, b, sample=True):
    """
    >>> uniform_real_distribution_test(0, 0)
    0.0
    >>> x = uniform_real_distribution_test(0, 5)
    >>> 0 < x and x < 5
    True
    >>> uniform_real_distribution_test(3, 8, False)
    (3.0, 8.0)
    """
    cdef uniform_real_distribution[double] dist = uniform_real_distribution[double](a, b)
    return sample_or_range[uniform_real_distribution[double]](dist, sample)


def bernoulli_distribution_test(proba, sample=True):
    """
    >>> bernoulli_distribution_test(0)
    False
    >>> bernoulli_distribution_test(1)
    True
    >>> bernoulli_distribution_test(0.7, False)
    (False, True)
    """
    cdef bernoulli_distribution dist = bernoulli_distribution(proba)
    return sample_or_range[bernoulli_distribution](dist, sample)


def binomial_distribution_test(n, proba, sample=True):
    """
    >>> binomial_distribution_test(10, 0)
    0
    >>> binomial_distribution_test(10, 1)
    10
    >>> x = binomial_distribution_test(100, 0.5)
    >>> 0 < x and x < 100  # Passes with high probability.
    True
    >>> binomial_distribution_test(75, 0.3, False)
    (0, 75)
    """
    cdef binomial_distribution[int] dist = binomial_distribution[int](n, proba)
    return sample_or_range[binomial_distribution[int]](dist, sample)


def geometric_distribution_test(proba, sample=True):
    """
    >>> geometric_distribution_test(1)
    0
    >>> geometric_distribution_test(1e-5) > 100  # Passes with high probability.
    True
    >>> geometric_distribution_test(0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef geometric_distribution[int] dist = geometric_distribution[int](proba)
    return sample_or_range[geometric_distribution[int]](dist, sample)


def negative_binomial_distribution_test(n, p, sample=True):
    """
    >>> negative_binomial_distribution_test(5, 0)  # 2147483647 = 2 ** 32 - 1
    2147483647
    >>> negative_binomial_distribution_test(5, 1)
    0
    >>> negative_binomial_distribution_test(10, 1e-5) > 100  # Passes with high probability.
    True
    >>> negative_binomial_distribution_test(10, 0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef negative_binomial_distribution[int] dist = negative_binomial_distribution[int](n, p)
    return sample_or_range[negative_binomial_distribution[int]](dist, sample)


def poisson_distribution_test(rate, sample=True):
    """
    >>> poisson_distribution_test(0)
    0
    >>> x = poisson_distribution_test(1000)  # Passes with high probability.
    >>> 900 < x and x < 1100
    True
    >>> poisson_distribution_test(7, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef poisson_distribution[int] dist = poisson_distribution[int](rate)
    return sample_or_range[poisson_distribution[int]](dist, sample)
