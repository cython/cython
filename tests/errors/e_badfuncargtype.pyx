# mode: error

cdef struct Spam

cdef extern i32 spam(void)            # function argument cannot be void
cdef extern i32 grail(i32 i, void v)  # function argument cannot be void
fn i32 tomato(Spam s):                # incomplete type
    pass

_ERRORS = u"""
5:21: Use spam() rather than spam(void) to declare a function with no arguments.
6:29: Use spam() rather than spam(void) to declare a function with no arguments.
7:14: Argument type 'Spam' is incomplete
"""
