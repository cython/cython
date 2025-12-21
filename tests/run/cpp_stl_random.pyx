# mode: run
# tag: cpp, cpp11, no-cpp-locals

from libcpp.random cimport mt19937, mt19937_64, random_device, uniform_int_distribution, \
    uniform_real_distribution, bernoulli_distribution, binomial_distribution, \
    geometric_distribution, negative_binomial_distribution, poisson_distribution, \
    exponential_distribution, gamma_distribution, weibull_distribution, \
    extreme_value_distribution, normal_distribution, lognormal_distribution, \
    chi_squared_distribution, cauchy_distribution, fisher_f_distribution, student_t_distribution
from libc.float cimport DBL_MAX as DBL_MAX_


DBL_MAX = DBL_MAX_


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


ctypedef fused any_dist:
    uniform_int_distribution[int]
    uniform_real_distribution[double]
    bernoulli_distribution
    binomial_distribution[int]
    geometric_distribution[int]
    negative_binomial_distribution[int]
    poisson_distribution[int]
    exponential_distribution[double]
    gamma_distribution[double]
    weibull_distribution[double]
    extreme_value_distribution[double]
    normal_distribution[double]
    lognormal_distribution[double]
    chi_squared_distribution[double]
    cauchy_distribution[double]
    fisher_f_distribution[double]
    student_t_distribution[double]


cdef sample_or_range(any_dist dist, bint sample):
    """
    This helper function returns a sample if `sample` is truthy and the range of the distribution
    if `sample` is falsy. We use a fused type to avoid duplicating the conditional statement in each
    distribution test.
    """
    cdef random_device rd
    if sample:
        dist(mt19937(rd()))
    else:
        return dist.min(), dist.max()


def uniform_int_distribution_test(a, b, sample=True):
    """
    >>> uniform_int_distribution_test(2, 3)
    >>> uniform_int_distribution_test(5, 9, False)
    (5, 9)
    """
    cdef uniform_int_distribution[int] dist = uniform_int_distribution[int](a, b)
    return sample_or_range[uniform_int_distribution[int]](dist, sample)


def uniform_real_distribution_test(a, b, sample=True):
    """
    >>> x = uniform_real_distribution_test(4, 5)
    >>> uniform_real_distribution_test(3, 8, False)
    (3.0, 8.0)
    """
    cdef uniform_real_distribution[double] dist = uniform_real_distribution[double](a, b)
    return sample_or_range[uniform_real_distribution[double]](dist, sample)


def bernoulli_distribution_test(proba, sample=True):
    """
    >>> bernoulli_distribution_test(0.2)
    >>> bernoulli_distribution_test(0.7, False)
    (False, True)
    """
    cdef bernoulli_distribution dist = bernoulli_distribution(proba)
    return sample_or_range[bernoulli_distribution](dist, sample)


def binomial_distribution_test(n, proba, sample=True):
    """
    >>> binomial_distribution_test(10, 0.7)
    >>> binomial_distribution_test(75, 0.3, False)
    (0, 75)
    """
    cdef binomial_distribution[int] dist = binomial_distribution[int](n, proba)
    return sample_or_range[binomial_distribution[int]](dist, sample)


def geometric_distribution_test(proba, sample=True):
    """
    >>> geometric_distribution_test(.4)
    >>> geometric_distribution_test(0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef geometric_distribution[int] dist = geometric_distribution[int](proba)
    return sample_or_range[geometric_distribution[int]](dist, sample)


def negative_binomial_distribution_test(n, p, sample=True):
    """
    >>> negative_binomial_distribution_test(5, .1)
    >>> negative_binomial_distribution_test(10, 0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef negative_binomial_distribution[int] dist = negative_binomial_distribution[int](n, p)
    return sample_or_range[negative_binomial_distribution[int]](dist, sample)


def poisson_distribution_test(rate, sample=True):
    """
    >>> poisson_distribution_test(7)
    >>> poisson_distribution_test(7, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef poisson_distribution[int] dist = poisson_distribution[int](rate)
    return sample_or_range[poisson_distribution[int]](dist, sample)


def exponential_distribution_test(rate, sample=True):
    """
    >>> x = exponential_distribution_test(6)
    >>> l, u = exponential_distribution_test(1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef exponential_distribution[double] dist = exponential_distribution[double](rate)
    return sample_or_range[exponential_distribution[double]](dist, sample)


def gamma_distribution_test(shape, scale, sample=True):
    """
    >>> gamma_distribution_test(3, 4)
    >>> l, u = gamma_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef gamma_distribution[double] dist = gamma_distribution[double](shape, scale)
    return sample_or_range[gamma_distribution[double]](dist, sample)


def weibull_distribution_test(shape, scale, sample=True):
    """
    >>> weibull_distribution_test(3, 2)
    >>> l, u = weibull_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef weibull_distribution[double] dist = weibull_distribution[double](shape, scale)
    return sample_or_range[weibull_distribution[double]](dist, sample)


def extreme_value_distribution_test(shape, scale, sample=True):
    """
    >>> extreme_value_distribution_test(3, 0.1)
    >>> l, u = extreme_value_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef extreme_value_distribution[double] dist = extreme_value_distribution[double](shape, scale)
    return sample_or_range[extreme_value_distribution[double]](dist, sample)


def normal_distribution_test(loc, scale, sample=True):
    """
    >>> normal_distribution_test(3, 2)
    >>> l, u = normal_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef normal_distribution[double] dist = normal_distribution[double](loc, scale)
    return sample_or_range[normal_distribution[double]](dist, sample)


def lognormal_distribution_test(loc, scale, sample=True):
    """
    >>> lognormal_distribution_test(3, 2)
    >>> l, u = lognormal_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef lognormal_distribution[double] dist = lognormal_distribution[double](loc, scale)
    return sample_or_range[lognormal_distribution[double]](dist, sample)


def chi_squared_distribution_test(dof, sample=True):
    """
    >>> x = chi_squared_distribution_test(9)
    >>> l, u = chi_squared_distribution_test(5, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef chi_squared_distribution[double] dist = chi_squared_distribution[double](dof)
    return sample_or_range[chi_squared_distribution[double]](dist, sample)


def cauchy_distribution_test(loc, scale, sample=True):
    """
    >>> cauchy_distribution_test(3, 9)
    >>> l, u = cauchy_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef cauchy_distribution[double] dist = cauchy_distribution[double](loc, scale)
    return sample_or_range[cauchy_distribution[double]](dist, sample)


def fisher_f_distribution_test(m, n, sample=True):
    """
    >>> x = fisher_f_distribution_test(9, 11)
    >>> l, u = fisher_f_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef fisher_f_distribution[double] dist = fisher_f_distribution[double](m, n)
    return sample_or_range[fisher_f_distribution[double]](dist, sample)


def student_t_distribution_test(dof, sample=True):
    """
    >>> x = student_t_distribution_test(13)
    >>> l, u = student_t_distribution_test(1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef student_t_distribution[double] dist = student_t_distribution[double](dof)
    return sample_or_range[student_t_distribution[double]](dist, sample)
