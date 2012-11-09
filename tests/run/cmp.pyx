def single_py(a, b):
    """
    >>> single_py(1, 2)
    True
    >>> single_py(2, 1)
    False
    """
    return a < b

def cascaded_py(a, b, c):
    """
    >>> cascaded_py(1, 2, 3)
    True
    >>> cascaded_py(1, 2, -1)
    False
    >>> cascaded_py(10, 2, 3)
    False
    """
    return a < b < c

def single_c(int a, int b):
    """
    >>> single_c(1, 2)
    True
    >>> single_c(2, 1)
    False
    """
    return a < b

def cascaded_c(double a, double b, double c):
    """
    >>> cascaded_c(1, 2, 3)
    True
    >>> cascaded_c(1, 2, -1)
    False
    >>> cascaded_c(10, 2, 3)
    False
    """
    return a < b < c

def cascaded_mix_pyleft(a, double b, double c):
    """
    >>> cascaded_mix_pyleft(1, 2, 3)
    True
    >>> cascaded_mix_pyleft(1, 2, -1)
    False
    >>> cascaded_mix_pyleft(10, 2, 3)
    False
    """
    return a < b < c

def cascaded_mix_pyright(double a, double b, c):
    """
    >>> cascaded_mix_pyright(1, 2, 3)
    True
    >>> cascaded_mix_pyright(1, 2, -1)
    False
    >>> cascaded_mix_pyright(10, 2, 3)
    False
    """
    return a < b < c

def typed_cmp(list L):
    """
    >>> typed_cmp([1,2,3])
    False
    False
    False
    False
    """
    print L is Ellipsis
    print Ellipsis is L
    print 1 == L
    print L == 1.5

def pointer_cmp():
    """
    >>> pointer_cmp()
    True
    False
    True
    """
    cdef int* a = NULL
    cdef double* b = NULL
    cdef double** c = NULL
    print a is NULL
    print b is not NULL
    print c == NULL

def c_cmp(double a, int b, long c):
    """
    >>> c_cmp(1, 2, 3)
    True
    >>> c_cmp(1.5, 2, 2)
    True
    >>> c_cmp(1.5, 2, 0)
    False
    >>> c_cmp(1, 1, 3)
    False
    """
    return a < b <= c
