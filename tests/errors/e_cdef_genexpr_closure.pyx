# mode: error

cpdef cpdef_genexpr():
    closed_over = 1
    return (closed_over for i in (1, 2, 3))


_ERRORS = u"""
3:0: closures inside cpdef functions not yet supported
"""
