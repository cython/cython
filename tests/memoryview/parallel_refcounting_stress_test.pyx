# mode: run
# tag: openmp

from cython.parallel cimport prange
cimport cython
from random import randint, random

include "../buffers/mockbuffers.pxi"

# This test is designed to pick up concurrency errors in memoryview reference counting.
# It won't be 100% reliable, but hopefully does enough memoryview reference counting in
# parallel that we should see errors if it isn't thread-safe.
# It has been verified to crash if the atomic reference counting is replaced with non-atomic counting.

@cython.boundscheck(False)
@cython.wraparound(False)
def refcounting_stress_test(int N):
    """
    >>> _ = refcounting_stress_test(5000)
    acquired a
    acquired b
    acquired c
    released a
    released b
    released c
    """
    selectors = [ randint(0, 3) for _ in range(N) ]
    cdef int[::1] selectorsview = IntMockBuffer(None, selectors, (N,))
    shape = (10, 3)
    size = shape[0]*shape[1]
    a = [ random() for _ in range(size) ]
    b = [ random() for _ in range(size) ]
    c = [ random() for _ in range(size) ]
    cdef double[:,:] aview = DoubleMockBuffer("a", a, shape)
    cdef double[:,:] bview = DoubleMockBuffer("b", b, shape)
    cdef double[:,:] cview = DoubleMockBuffer("c", c, shape)

    cdef int i
    cdef double total = 0.0

    for i in prange(N, nogil=True):
        total += loopbody(aview, bview, cview, selectorsview[i])

    # make "release" order predictable
    del aview
    del bview
    del cview

    return total

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double loopbody(double[:,:] a, double[:,:] b, double[:,:] c, int selector) nogil:
    cdef double[:,:] selected
    cdef double[:] subslice
    cdef double res = 0

    if selector % 3 == 1:
        selected = a
    elif selector % 3 == 2:
        selected = b
    else:
        selected = c

    for i in range(selected.shape[0]):
        subslice = selected[i, :]
        res += subslice[0] + subslice[2]
    return res
