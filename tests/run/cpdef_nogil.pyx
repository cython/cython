# cython: binding=True
# mode: run
# tag: cyfunction

cpdef int simple() nogil:
    """
    >>> simple()
    1
    """
    return 1


cpdef int call_nogil():
    """
    >>> call_nogil()
    1
    """
    with nogil:
        return simple()
