cdef struct Spam:
    char *grail

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
