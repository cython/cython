# cfunc version compiled in C
# returns bint and compares two ints

cdef bint c_compare(int a, int b):
    return a == b