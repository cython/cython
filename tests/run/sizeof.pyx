cdef struct Spam:
    char *grail

cdef extern from *:
    """
    typedef char ulong;
    """
    ctypedef int ulong

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

    # Cython should generate the C code "sizeof(ulong)"
    # rather than interpreting ulong as "unsigned long".
    return sizeof(ulong)
