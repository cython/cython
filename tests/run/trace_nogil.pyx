# cython: linetrace=True

cdef class MyError(Exception):
    """
    An  exception is raised when operation submission
    or execution encounters an error.
    """


cdef void foo(int err) nogil except *:
    with gil:
        raise MyError(err)


# Test from gh-4637
def handler(int err):
    """
    >>> handler(0)
    All good
    >>> handler(1)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    trace_nogil.MyError: 1
    """
    if (err % 2):
        with nogil:
            foo(err)
    else:
        print("All good")
