# mode: compile
# tag: fused, werror

"""
Very short test for https://github.com/cython/cython/issues/3492
(Needs its own file since werror fails on the main fused-test files)
wraparound and boundscheck directives shouldn't break the fused
dispatcher function
"""

cimport cython

ctypedef fused fused_t:
    str
    int
    long
    complex

@cython.wraparound(False)
@cython.boundscheck(False)
def func(fused_t a, cython.floating b):
    return a, b
