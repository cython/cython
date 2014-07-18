# mode: error

cpdef cpdef_yield():
    def inner():
        pass

_ERRORS = u"""
3:6: closures inside cpdef functions not yet supported
"""
