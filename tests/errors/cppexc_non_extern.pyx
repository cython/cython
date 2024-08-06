# mode: error
# tag: warnings, cpp

cdef inline void handle_exception():
    pass

# GH 3064 - cppfunc caused invalid code to be generated with +handle_exception
# error to prevent this
cdef test_func1(self) except +handle_exception:
    pass

# warning
cdef test_func2(self) except +:
    pass

_WARNINGS = """
9:5: Only extern functions can throw C++ exceptions.
13:5: Only extern functions can throw C++ exceptions.
"""
