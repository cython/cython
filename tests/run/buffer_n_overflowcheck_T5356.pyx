# mode: run
# ticket: t5356

cimport cython


@cython.overflowcheck(True)
cdef size_t _mul_checked(size_t a, size_t b) except? -1:
    return a * b


def f(unsigned char[:] a, unsigned char[:] b):
    """
    >>> f(memoryview(bytearray(b"12")), memoryview(bytearray(b"345")))
    6
    """
    return _mul_checked(a.shape[0], b.shape[0])
