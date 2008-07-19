
__doc__ = """
   >>> test(1, 2)
   4 1 2 2 0
   >>> A().value
   4
"""

cdef class A:
    cdef int value = 4

def test(x, int y):
    if True:
        before = 0
    cdef int a = 4, b = x, c = y, *p = &y
    print a, b, c, p[0], before

# Also test that pruning cdefs doesn't hurt 
def empty():
    cdef int i
