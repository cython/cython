# mode: error
# tag: restrict

ctypedef double* double_ptr

cdef void ok_ptr_typedef(double_ptr restrict p):
    pass

cdef void bad_int(int restrict x):
    pass

cdef void bad_object(object restrict o):
    pass

_ERRORS = """
9:22: Restrict qualifier can only be applied to pointer or memoryview types
12:28: Const/restrict base type cannot be a Python object
12:28: Restrict qualifier can only be applied to pointer or memoryview types
"""
