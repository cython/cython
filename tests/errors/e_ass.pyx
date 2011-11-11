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
x = y # error

cdef int_array *x_ptr = &x
x_ptr[0] = y # error

cdef class A:
    cdef int_array value
    def __init__(self):
        self.value = x # error

_ERRORS = u"""
17:2: Assignment to non-lvalue 'x'
20:5: Assignment to non-lvalue of type 'int_array'
25:12: Assignment to non-lvalue of type 'int_array'
7:19: Cannot assign type 'char *' to 'int'
8:20: Cannot convert Python object to 'int *'
10:20: Cannot convert 'int *' to Python object
"""
