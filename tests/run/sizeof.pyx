cdef struct Spam:
    char *grail

cdef extern from *:
    """
    typedef char p_ulong;
    """
    ctypedef int p_ulong

def f():
    """
    >>> f()
    """
    cdef int i, j, k
    cdef char *p
    i = sizeof(p)
    i = sizeof(j + k)
    i = sizeof(int)
    i = sizeof(long int)
    i = sizeof(void*)
    i = sizeof(Spam)
    i = sizeof(Spam*)
    i = sizeof(Spam[5])
    i = sizeof(Spam (*)())

def test_extern_typedef():
    """
    >>> test_extern_typedef()
    1
    """
    # Cython should generate the C code "sizeof(p_ulong)"
    # rather than interpreting p_ulong as "unsigned long*".
    return sizeof(p_ulong)
