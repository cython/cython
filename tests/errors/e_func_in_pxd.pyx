# mode: error

cimport e_func_in_pxd_support


_ERRORS = u"""
1:0: function definition in pxd file must be declared 'cdef inline'
4:0: inline function definition in pxd file cannot be 'public'
7:0: inline function definition in pxd file cannot be 'api'
"""
