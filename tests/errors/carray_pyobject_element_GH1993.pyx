# mode: error
# ticket: 1993

cdef class A:
    pass

cdef class B:
    cdef A ext_arr[100]
    cdef object obj_arr[3]

def f():
    cdef A local_arr[2]

_ERRORS = """
8:18: Array element cannot be a Python object
9:23: Array element cannot be a Python object
12:20: Array element cannot be a Python object
"""
