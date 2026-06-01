# mode: error
# tag: werror

cdef foo():
    pass

def foo():
    pass

_ERRORS = u"""
7:0: 'foo' redeclared
7:0: Overriding a c(p)def method with a def method. This can lead to different methods being called depending on the call context. Consider using a cpdef method for both.
"""
