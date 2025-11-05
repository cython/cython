# mode: error
# tag: warnings

cdef inline void handle_exception():
    pass

# GH 3064 - cppfunc caused invalid code to be generated with +handle_exception
# error to prevent this
cdef test_func1(self) except +handle_exception:
    pass

# warning
cdef test_func2(self) except +:
    pass


_ERRORS = """
9:0: Only extern functions can throw C++ exceptions.
"""

_WARNINGS = """
13:0: Only extern functions can throw C++ exceptions.
"""
