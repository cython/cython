# mode: error

# cpdef generators are still rejected (yield inside cpdef body with a closure).
cpdef cpdef_yield():
    def inner():
        pass
    yield inner()


_ERRORS = u"""
4:0: cpdef generators are not supported with 'cpdef' syntax; use a 'def' function with @cython.ccall (or auto_cpdef)
7:4: 'yield' not supported here
"""
