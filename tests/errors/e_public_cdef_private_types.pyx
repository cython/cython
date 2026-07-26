# mode: error

ctypedef char *string_t
ctypedef public char *public_string_t
ctypedef api char *api_string_t

# This should all fail
cdef public pub_func1(string_t x):
    pass

cdef api api_func1(string_t x):
    pass

cdef public string_t pub_func2():
    pass

cdef api string_t api_func2():
    pass

cdef public opt_pub_func(x = None):
    pass

cdef api opt_api_func(x = None):
    pass

# This should all work
cdef public pub_func3(public_string_t x, api_string_t y):
    pass

cdef api api_func3(public_string_t x, api_string_t y):
    pass

cdef opt_func(x = None):
    pass

_ERRORS = u"""
e_public_cdef_private_types.pyx:8:22: Function declared public or api may not have private types
e_public_cdef_private_types.pyx:11:19: Function declared public or api may not have private types
e_public_cdef_private_types.pyx:14:0: Function declared public or api may not have private types
e_public_cdef_private_types.pyx:17:0: Function declared public or api may not have private types
e_public_cdef_private_types.pyx:20:24: Function with optional arguments may not be declared public or api
e_public_cdef_private_types.pyx:23:21: Function with optional arguments may not be declared public or api
"""
