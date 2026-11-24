# mode: run
# tag: refnanny

# runtests.py excludes the tests tagged "refnanny" when it runs without reference
# count checking (--no-refnanny, PyPy, GraalPy).  Otherwise, it must compile all tests
# with CYTHON_REFNANNY, also in the worker processes of parallel test runs (-jN),
# which do not inherit its state from the main process unless they are forked.

cdef extern from *:
    const bint CYTHON_REFNANNY


def compiled_with_refnanny():
    """
    >>> compiled_with_refnanny()
    True
    """
    return CYTHON_REFNANNY
