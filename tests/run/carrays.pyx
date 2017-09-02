def test1():
    """
    >>> test1()
    2
    """
    cdef int[2][2] x
    x[0][0] = 1
    x[0][1] = 2
    x[1][0] = 3
    x[1][1] = 4
    return f(x)[1]

cdef int* f(int x[2][2]):
    return x[0]


def assign_index_in_loop():
    """
    >>> assign_index_in_loop()
    2
    """
    cdef int i = 0
    cdef int[1] a
    cdef int[1] b
    for a[0], b[0] in enumerate(range(3)):
        assert a[0] == b[0]
        assert a[0] == i
        i += 1

    assert a[0] == b[0]
    return b[0]


def test2():
    """
    >>> test2()
    0
    """
    cdef int[5] a1
    cdef int a2[2+3]
    return sizeof(a1) - sizeof(a2)

cdef enum:
    MY_SIZE_A = 2
    MY_SIZE_B = 3

def test3():
    """
    >>> test3()
    (2, 3)
    """
    cdef int a[MY_SIZE_A]
    cdef int b[MY_SIZE_B]
    return sizeof(a)/sizeof(int), sizeof(b)/sizeof(int)


from libc cimport limits

def test_cimported_attribute():
    """
    >>> test_cimported_attribute()
    True
    """
    cdef char a[limits.CHAR_MAX]
    return sizeof(a) >= 127
