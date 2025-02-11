
cdef inline int my_add(int a, int b=1, int c=0):
    return a + b + c

cdef inline index(list L):
    # This function should *not* be affected by directives set in the outer scope, such as "wraparound".
    # See https://github.com/cython/cython/issues/1071
    return L[-1]

cdef inline call_index(list L):
    return index(L)
