# mode: error
# tag: werror

fn foo():
    pass

def foo():
    pass

_ERRORS = u"""
7:0: 'foo' redeclared
7:0: Overriding cdef method with def method.
"""
