
cdef inline int my_add(int a, int b=1, int c=0):
    return a + b + c

cdef inline index(double[::1] arr):
    # this function should *not* be affected by directives set in the outer scope
    # (issue 1071)
    return arr[-1]
