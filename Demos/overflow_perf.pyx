# cython: language_level=3
# distutils: extra_compile_args = -O3

cimport cython

ctypedef fused INT:
    int
    long long
    unsigned int
    unsigned long long
    object

ctypedef fused C_INT:
    int
    long long
    unsigned int
    unsigned long long


@cython.overflowcheck(False)
def fib(INT n):
    """
    >>> [fib(k) for k in range(10)]
    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    cdef INT a, b, k
    a, b = 0, 1
    for k in range(n):
        a, b = b, a + b
    return int(b)


@cython.overflowcheck(True)
def fib_overflow(INT n):
    """
    >>> [fib_overflow(k) for k in range(10)]
    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    cdef INT a, b, k
    a, b = 0, 1
    for k in range(n):
        a, b = b, a + b
    return int(b)


@cython.overflowcheck(False)
def collatz(INT n):
    """
    >>> collatz(1)
    0
    >>> collatz(5)
    5
    >>> collatz(10)
    6
    """
    cdef INT k = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3*n + 1
        k += 1
    return int(k)


@cython.overflowcheck(True)
@cython.overflowcheck.fold(False)
def collatz_overflow(INT n):
    """
    >>> collatz_overflow(1)
    0
    >>> collatz_overflow(5)
    5
    >>> collatz_overflow(10)
    6
    """
    cdef INT k = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3*n + 1
        k += 1
    return int(k)


@cython.overflowcheck(True)
@cython.overflowcheck.fold(True)
def collatz_overflow_fold(INT n):
    """
    >>> collatz_overflow_fold(1)
    0
    >>> collatz_overflow_fold(5)
    5
    >>> collatz_overflow_fold(10)
    6
    """
    cdef INT k = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3*n + 1
        k += 1
    return int(k)


@cython.overflowcheck(False)
def factorial(INT n):
    """
    >>> factorial(2)
    2
    >>> factorial(5)
    120
    """
    cdef INT k, res = 1
    for k in range(2, n+1):
        res = res * k
    return int(res)

@cython.overflowcheck(True)
def factorial_overflow(INT n):
    """
    >>> factorial_overflow(2)
    2
    >>> factorial_overflow(5)
    120
    """
    cdef INT k, res = 1
    for k in range(2, n+1):
        res = res * k
    return int(res)


@cython.overflowcheck(False)
def most_orthogonal(C_INT[:,::1] vectors):
    cdef C_INT n = vectors.shape[0]
    cdef C_INT* a
    cdef C_INT* b
    cdef double min_dot = 2 # actual max is 1
    for i in range(n):
        for j in range(i):
            a = &vectors[i, 0]
            b = &vectors[j, 0]
            # A highly nested arithmetic expression...
            normalized_dot = (1.0 * (a[0]*b[0] + a[1]*b[1] + a[2]*b[2]) /
                ((a[0]*a[0] + a[1]*a[1] + a[2]*a[2]) * (b[0]*b[0] + b[1]*b[1]+b[2]*b[2])))
            if normalized_dot < min_dot:
                min_dot = normalized_dot
                min_pair = i, j
    return vectors[i], vectors[j]


@cython.overflowcheck(True)
@cython.overflowcheck.fold(False)
def most_orthogonal_overflow(C_INT[:,::1] vectors):
    cdef C_INT n = vectors.shape[0]
    cdef C_INT* a
    cdef C_INT* b
    cdef double min_dot = 2 # actual max is 1
    for i in range(n):
        for j in range(i):
            a = &vectors[i, 0]
            b = &vectors[j, 0]
            # A highly nested arithmetic expression...
            normalized_dot = ((a[0]*b[0] + a[1]*b[1] + a[2]*b[2]) /
                (1.0 * (a[0]*a[0] + a[1]*a[1] + a[2]*a[2]) * (b[0]*b[0] + b[1]*b[1]+b[2]*b[2])))
            if normalized_dot < min_dot:
                min_dot = normalized_dot
                min_pair = i, j
    return vectors[i], vectors[j]


@cython.overflowcheck(True)
@cython.overflowcheck.fold(True)
def most_orthogonal_overflow_fold(C_INT[:,::1] vectors):
    cdef C_INT n = vectors.shape[0]
    cdef C_INT* a
    cdef C_INT* b
    cdef double min_dot = 2 # actual max is 1
    for i in range(n):
        for j in range(i):
            a = &vectors[i, 0]
            b = &vectors[j, 0]
            # A highly nested arithmetic expression...
            normalized_dot = ((a[0]*b[0] + a[1]*b[1] + a[2]*b[2]) /
                (1.0 * (a[0]*a[0] + a[1]*a[1] + a[2]*a[2]) * (b[0]*b[0] + b[1]*b[1]+b[2]*b[2])))
            if normalized_dot < min_dot:
                min_dot = normalized_dot
                min_pair = i, j
    return vectors[i], vectors[j]
