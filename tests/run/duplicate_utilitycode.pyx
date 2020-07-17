# mode: run

# There were a few cases where duplicate utility code definitions (i.e. with the same name)
# could be generated, causing C compile errors. This file tests them.

from __future__ import print_function

cdef f1(x, r):
    return "f1"

cdef f2(x1, r):
    return "f2"

def make_map():
    """
    https://github.com/cython/cython/issues/3716
    This is testing the generation of wrappers for f1 and f2
    >>> for k, f in make_map().items():
    ...    print(k == f(0, 0))  # in both cases the functions should just return their name
    True
    True
    """
    cdef map = {
        "f1": f1,
        "f2": f2,
    }
    return map
