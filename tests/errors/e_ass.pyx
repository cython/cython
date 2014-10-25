# mode: error

cdef void foo(obj):
    cdef int i1
    cdef char *p1
    cdef int *p2
    i1 = p1 # error
    p2 = obj # error

    obj = p2 # error


ctypedef int[1] int_array


cdef int_array x, y
x = y  # not an error

cdef int_array *x_ptr = &x
x_ptr[0] = y  # not an error

cdef class A:
    cdef int_array value
    def __init__(self):
        self.value = x  # not an error


ctypedef int[2] int_array2

cdef int_array2 z
z = x  # error


cdef enum:
    SIZE = 2

ctypedef int[SIZE] int_array_dyn

cdef int_array_dyn d
d = z  # error


_ERRORS = u"""
7:19: Cannot assign type 'char *' to 'int'
8:20: Cannot convert Python object to 'int *'
10:20: Cannot convert 'int *' to Python object
31:14: Cannot assign type 'int_array' to 'int_array2'
40:14: Cannot assign type 'int_array2' to 'int_array_dyn'
"""
