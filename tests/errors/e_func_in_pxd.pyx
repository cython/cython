# mode: error

cimport e_func_in_pxd_support

_ERRORS = u"""
1:5: function definition in pxd file must be declared 'cdef inline'
4:5: inline function definition in pxd file cannot be 'public'
7:5: inline function definition in pxd file cannot be 'api'
"""
