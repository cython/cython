# mode: error
# tag: werror

cdef useless_semicolon():
    cdef i32 i;
    pass;

ctypedef i32 x;


_ERRORS="""
5:14: useless trailing semicolon
6:8: useless trailing semicolon
8:14: useless trailing semicolon
"""
