# mode: run
# tag: cpp, cpp11

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
    let mt19937 gen = mt19937(42)
    return gen()

def mt19937_reseed_test():
    """
    >>> print(mt19937_reseed_test())
    1608637542
    """
    let mt19937 gen
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
    let mt19937 gen
    return gen.min(), gen.max()

def mt19937_discard(z):
    """
    >>> x, y = mt19937_discard(13)
    >>> print(x)
    1972458954
    >>> print(y)
    1972458954
    """
    let mt19937 gen = mt19937(42)
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
    let mt19937_64 gen = mt19937_64(42)
    return gen()

def mt19937_64_reseed_test():
    """
    >>> print(mt19937_64_reseed_test())
    13930160852258120406
    """
    let mt19937_64 gen
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
    let mt19937_64 gen
    return gen.min(), gen.max()

def mt19937_64_discard(z):
    """
    >>> x, y = mt19937_64_discard(13)
    >>> print(x)
    11756813601242511406
    >>> print(y)
    11756813601242511406
    """
    let mt19937_64 gen = mt19937_64(42)
    # Throw away z random numbers.
    gen.discard(z)
    a = gen()

    # Iterate over z random numbers.
    gen.seed(42)
    for _ in range(z + 1):
        b = gen()
    return a, b

ctypedef fused any_dist:
    uniform_int_distribution[i32]
    uniform_real_distribution[f64]
    bernoulli_distribution
    binomial_distribution[i32]
    geometric_distribution[i32]
    negative_binomial_distribution[i32]
    poisson_distribution[i32]
    exponential_distribution[f64]
    gamma_distribution[f64]
    weibull_distribution[f64]
    extreme_value_distribution[f64]
    normal_distribution[f64]
    lognormal_distribution[f64]
    chi_squared_distribution[f64]
    cauchy_distribution[f64]
    fisher_f_distribution[f64]
    student_t_distribution[f64]

cdef sample_or_range(any_dist dist, bint sample):
    """
    This helper function returns a sample if `sample` is truthy and the range of the distribution
    if `sample` is falsy. We use a fused type to avoid duplicating the conditional statement in each
    distribution test.
    """
    let random_device rd
    if sample:
        dist(mt19937(rd()))
    else:
        return dist.min(), dist.max()

def uniform_int_distribution_test(a, b, sample=true):
    """
    >>> uniform_int_distribution_test(2, 3)
    >>> uniform_int_distribution_test(5, 9, False)
    (5, 9)
    """
    let uniform_int_distribution[i32] dist = uniform_int_distribution[i32](a, b)
    return sample_or_range[uniform_int_distribution[i32]](dist, sample)

def uniform_real_distribution_test(a, b, sample=true):
    """
    >>> x = uniform_real_distribution_test(4, 5)
    >>> uniform_real_distribution_test(3, 8, False)
    (3.0, 8.0)
    """
    let uniform_real_distribution[f64] dist = uniform_real_distribution[f64](a, b)
    return sample_or_range[uniform_real_distribution[f64]](dist, sample)

def bernoulli_distribution_test(proba, sample=true):
    """
    >>> bernoulli_distribution_test(0.2)
    >>> bernoulli_distribution_test(0.7, False)
    (False, True)
    """
    let bernoulli_distribution dist = bernoulli_distribution(proba)
    return sample_or_range[bernoulli_distribution](dist, sample)

def binomial_distribution_test(n, proba, sample=true):
    """
    >>> binomial_distribution_test(10, 0.7)
    >>> binomial_distribution_test(75, 0.3, False)
    (0, 75)
    """
    let binomial_distribution[i32] dist = binomial_distribution[i32](n, proba)
    return sample_or_range[binomial_distribution[i32]](dist, sample)

def geometric_distribution_test(proba, sample=true):
    """
    >>> geometric_distribution_test(.4)
    >>> geometric_distribution_test(0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    let geometric_distribution[i32] dist = geometric_distribution[i32](proba)
    return sample_or_range[geometric_distribution[i32]](dist, sample)

def negative_binomial_distribution_test(n, p, sample=true):
    """
    >>> negative_binomial_distribution_test(5, .1)
    >>> negative_binomial_distribution_test(10, 0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    let negative_binomial_distribution[i32] dist = negative_binomial_distribution[i32](n, p)
    return sample_or_range[negative_binomial_distribution[i32]](dist, sample)

def poisson_distribution_test(rate, sample=true):
    """
    >>> poisson_distribution_test(7)
    >>> poisson_distribution_test(7, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    let poisson_distribution[i32] dist = poisson_distribution[i32](rate)
    return sample_or_range[poisson_distribution[i32]](dist, sample)

def exponential_distribution_test(rate, sample=true):
    """
    >>> x = exponential_distribution_test(6)
    >>> l, u = exponential_distribution_test(1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let exponential_distribution[f64] dist = exponential_distribution[f64](rate)
    return sample_or_range[exponential_distribution[f64]](dist, sample)

def gamma_distribution_test(shape, scale, sample=true):
    """
    >>> gamma_distribution_test(3, 4)
    >>> l, u = gamma_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let gamma_distribution[f64] dist = gamma_distribution[f64](shape, scale)
    return sample_or_range[gamma_distribution[f64]](dist, sample)

def weibull_distribution_test(shape, scale, sample=true):
    """
    >>> weibull_distribution_test(3, 2)
    >>> l, u = weibull_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let weibull_distribution[f64] dist = weibull_distribution[f64](shape, scale)
    return sample_or_range[weibull_distribution[f64]](dist, sample)

def extreme_value_distribution_test(shape, scale, sample=true):
    """
    >>> extreme_value_distribution_test(3, 0.1)
    >>> l, u = extreme_value_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let extreme_value_distribution[f64] dist = extreme_value_distribution[f64](shape, scale)
    return sample_or_range[extreme_value_distribution[f64]](dist, sample)

def normal_distribution_test(loc, scale, sample=true):
    """
    >>> normal_distribution_test(3, 2)
    >>> l, u = normal_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let normal_distribution[f64] dist = normal_distribution[f64](loc, scale)
    return sample_or_range[normal_distribution[f64]](dist, sample)

def lognormal_distribution_test(loc, scale, sample=true):
    """
    >>> lognormal_distribution_test(3, 2)
    >>> l, u = lognormal_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let lognormal_distribution[f64] dist = lognormal_distribution[f64](loc, scale)
    return sample_or_range[lognormal_distribution[f64]](dist, sample)

def chi_squared_distribution_test(dof, sample=true):
    """
    >>> x = chi_squared_distribution_test(9)
    >>> l, u = chi_squared_distribution_test(5, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let chi_squared_distribution[f64] dist = chi_squared_distribution[f64](dof)
    return sample_or_range[chi_squared_distribution[f64]](dist, sample)

def cauchy_distribution_test(loc, scale, sample=true):
    """
    >>> cauchy_distribution_test(3, 9)
    >>> l, u = cauchy_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let cauchy_distribution[f64] dist = cauchy_distribution[f64](loc, scale)
    return sample_or_range[cauchy_distribution[f64]](dist, sample)

def fisher_f_distribution_test(m, n, sample=true):
    """
    >>> x = fisher_f_distribution_test(9, 11)
    >>> l, u = fisher_f_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let fisher_f_distribution[f64] dist = fisher_f_distribution[f64](m, n)
    return sample_or_range[fisher_f_distribution[f64]](dist, sample)

def student_t_distribution_test(dof, sample=true):
    """
    >>> x = student_t_distribution_test(13)
    >>> l, u = student_t_distribution_test(1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    let student_t_distribution[f64] dist = student_t_distribution[f64](dof)
    return sample_or_range[student_t_distribution[f64]](dist, sample)
