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

@cython.boundscheck(false)
@cython.wraparound(false)
def refcounting_stress_test(i32 N):
    """
    >>> _ = refcounting_stress_test(5000)
    acquired a
    acquired b
    acquired c
    released a
    released b
    released c
    """
    selectors = [randint(0, 3) for _ in range(N)]
    let i32[::1] selectorsview = IntMockBuffer(None, selectors, (N,))
    shape = (10, 3)
    size = shape[0]*shape[1]
    a = [random() for _ in range(size)]
    b = [random() for _ in range(size)]
    c = [random() for _ in range(size)]
    let f64[:, :] aview = DoubleMockBuffer("a", a, shape)
    let f64[:, :] bview = DoubleMockBuffer("b", b, shape)
    let f64[:, :] cview = DoubleMockBuffer("c", c, shape)

    let i32 i
    let f64 total = 0.0

    for i in prange(N, nogil=true):
        total += loopbody(aview, bview, cview, selectorsview[i])

    # make "release" order predictable
    del aview
    del bview
    del cview

    return total

@cython.boundscheck(false)
@cython.wraparound(false)
fn f64 loopbody(f64[:, :] a, f64[:, :] b, f64[:, :] c, i32 selector) nogil:
    let f64[:, :] selected
    let f64[:] subslice
    let f64 res = 0

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
