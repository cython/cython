from cython cimport typeof

def test(ptrdiff_t i):
    """
    >>> int(test(0))
    0
    >>> int(test(1))
    1
    >>> int(test(2))
    2
    >>> int(test(-1))
    -1
    >>> int(test(-2))
    -2
    >>> int(test((1<<31)-1))
    2147483647
    """
    return i

cdef class A:
    """
    >>> try: test(1<<200)
    ... except (OverflowError, TypeError): print("ERROR")
    ERROR

    >>> a = A(1,2)
    >>> a.a == 1
    True
    >>> a.b == 2
    True
    >>> print(a.foo(5))
    5
    >>> try: a.foo(1<<200)
    ... except (OverflowError, TypeError): print("ERROR")
    ERROR
    """
    cdef public ptrdiff_t a
    cdef readonly ptrdiff_t b

    def __init__(self, ptrdiff_t a, object b):
        self.a = a
        self.b = b

    cpdef ptrdiff_t foo(self, ptrdiff_t x):
        cdef object o = x
        return o

def test_types():
    """
    >>> test_types()
    """
    cdef int a = 1, b = 2
    assert typeof(&a - &b) == "ptrdiff_t", typeof(&a - &b)
    assert typeof((&a - &b) + 1) == "ptrdiff_t", typeof((&a - &b) + 1)
    assert typeof(&a + (&b - &a)) == "int *", typeof(&a + (&b - &a))
