# mode: run
# tag: memoryview, restrict
# cython: test_assert_c_code_has = CYTHON_UNUSED char \*CYTHON_RESTRICT __pyx_dp_v_y
# cython: test_assert_c_code_has = static CYTHON_FORCE_INLINE void __pyx_ri_f_16memview_restrict_saxpy\(
# cython: test_assert_c_code_has = __pyx_dp_v_plain_arg = __pyx_v_plain_arg.data;

cimport cython

from array import array


cdef void saxpy(const double[::1] restrict x, double[::1] restrict y, double alpha) noexcept nogil:
    cdef Py_ssize_t i
    for i in range(y.shape[0]):
        y[i] = alpha * x[i] + y[i]


def test_saxpy():
    """
    >>> test_saxpy()
    [3.0, 5.0, 7.0]
    """
    x = array('d', [1.0, 2.0, 3.0])
    y = array('d', [1.0, 1.0, 1.0])
    saxpy(x, y, 2.0)
    return list(y)


def def_function(double[:, :] restrict m, int restrict):
    """
    'restrict' can still be used as an argument name.

    >>> import array
    >>> data = array.array('d', range(6))
    >>> def_function(memoryview(data).cast('B').cast('d', (2, 3)), 10)
    14.0
    """
    return m[1, 1] + restrict


def def_function_star_args(double[::1] restrict a, *args, **kwargs):
    """
    >>> def_function_star_args(array('d', [1.0, 2.0]), 1, 2, x=3)
    (2.0, 2, 1)
    """
    return a[1], len(args), len(kwargs)


def plain_and_restrict(double[::1] plain_arg, double[::1] restrict r):
    """
    A non-restrict memoryview argument uses a local pointer copy.

    >>> plain_and_restrict(array('d', [1.0]), array('d', [2.0]))
    3.0
    """
    return plain_arg[0] + r[0]


cdef int strided_2d(double[:, :] restrict a, double[:, :] restrict b) except -1:
    cdef Py_ssize_t i, j
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            b[i, j] = a[i, j] * 2
    return 0


def test_strided_2d():
    """
    >>> test_strided_2d()
    [0.0, 2.0, 4.0, 6.0]
    """
    a = array('d', [0.0, 1.0, 2.0, 3.0])
    b = array('d', [0.0] * 4)
    strided_2d(memoryview(a).cast('B').cast('d', (2, 2)), memoryview(b).cast('B').cast('d', (2, 2)))
    return list(b)


cdef double recursive_sum(double[::1] restrict a, Py_ssize_t n) noexcept:
    if n == 0:
        return 0
    return a[n - 1] + recursive_sum(a, n - 1)


def test_recursion():
    """
    >>> test_recursion()
    10.0
    """
    a = array('d', [1.0, 2.0, 3.0, 4.0])
    return recursive_sum(a, 4)


def reassigned(double[::1] restrict a, double[::1] b):
    """
    Reassigned arguments are not hoisted, their data pointer changes.

    >>> reassigned(array('d', [1.0]), array('d', [5.0]))
    (1.0, 5.0)
    """
    first = a[0]
    a = b
    return first, a[0]


def closure(double[::1] restrict a):
    """
    Arguments used in closures are not hoisted.

    >>> closure(array('d', [1.0, 2.0]))
    3.0
    """
    def inner():
        return a[0] + a[1]
    return inner()


def slicing(double[::1] restrict a):
    """
    >>> slicing(array('d', [1.0, 2.0, 3.0]))
    (2.0, [2.0, 3.0])
    """
    cdef double[::1] s = a[1:]
    return s[0], list(s)


cdef double opt_args(double[::1] restrict a, double scale=2.0) except? -1:
    if a.shape[0] == 0:
        raise ValueError("empty")
    return a[0] * scale


def test_opt_args(values=(1.0,)):
    """
    >>> test_opt_args()
    (2.0, 3.0)
    >>> test_opt_args(())
    Traceback (most recent call last):
    ValueError: empty
    """
    a = array('d', values)
    return opt_args(a), opt_args(a, 3.0)


cpdef double cpdef_function(double[::1] restrict a, double[::1] restrict b):
    """
    >>> cpdef_function(array('d', [1.0]), array('d', [2.0]))
    3.0
    """
    return a[0] + b[0]


ctypedef fused number:
    int
    double


cdef number fused_sum(number[::1] restrict a, number[::1] restrict out) noexcept:
    cdef Py_ssize_t i
    for i in range(a.shape[0]):
        out[0] += a[i]
    return out[0]


def test_fused():
    """
    >>> test_fused()
    (6, 6.0)
    """
    cdef int[::1] i_in = array('i', [1, 2, 3])
    cdef int[::1] i_out = array('i', [0])
    cdef double[::1] d_in = array('d', [1.0, 2.0, 3.0])
    cdef double[::1] d_out = array('d', [0.0])
    return fused_sum(i_in, i_out), fused_sum(d_in, d_out)


cdef class Holder:
    cdef double factor

    def __init__(self, factor):
        self.factor = factor

    cdef double scaled(self, double[::1] restrict a) noexcept:
        return a[0] * self.factor

    def py_scaled(self, double[::1] restrict a):
        """
        >>> Holder(2.0).py_scaled(array('d', [3.0]))
        (6.0, 6.0)
        """
        return self.scaled(a), a[0] * self.factor


def none_argument(double[::1] restrict a=None):
    """
    >>> none_argument()
    True
    >>> none_argument(array('d', [1.0]))
    1.0
    """
    if a is None:
        return True
    return a[0]
