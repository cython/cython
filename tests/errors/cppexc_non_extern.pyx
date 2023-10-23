# mode: error
# tag: warnings

fn inline void handle_exception():
    pass

# GH 3064 - cppfunc caused invalid code to be generated with +handle_exception
# error to prevent this
fn test_func1(self) except +handle_exception:
    pass

# warning
fn test_func2(self) except +:
    pass

_ERRORS = """
9:0: Only extern functions can throw C++ exceptions.
"""

_WARNINGS = """
13:0: Only extern functions can throw C++ exceptions.
"""
